import logging
import re
import uuid
from datetime import UTC, datetime
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.document import DocumentChunk, UploadedDocument
from app.models.user import User
from app.rag.answer_service import AnswerService
from app.rag.document_summary_service import document_summary_service
from app.rag.file_parser import FileParser, UNSUPPORTED_FILE_MESSAGE
from app.rag.text_chunker import TextChunker
from app.rag.vector_store import SearchHit, VectorSearchService
from app.schemas.document import DocumentAskResponse, DocumentCitation, DocumentDeleteResponse, DocumentRead


logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self) -> None:
        self.parser = FileParser()
        self.chunker = TextChunker()
        self.vector_search = VectorSearchService()
        self.answer_service = AnswerService()

    async def upload_document(
        self,
        db: Session,
        user_id: uuid.UUID,
        file: UploadFile,
        title: str | None = None,
    ) -> DocumentRead:
        self._ensure_user_exists(db, user_id)
        self._validate_upload(file)

        document_id = uuid.uuid4()
        storage_path, file_size = await self._save_upload(file, user_id, document_id)
        document = UploadedDocument(
            id=document_id,
            user_id=user_id,
            title=title or self._title_from_filename(file.filename or "Untitled document"),
            original_filename=file.filename or "uploaded-document",
            mime_type=file.content_type or "application/octet-stream",
            file_size_bytes=file_size,
            storage_provider="local",
            storage_path=str(storage_path),
            status="processing",
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        try:
            parsed_document = self.parser.parse(
                storage_path,
                document.mime_type,
                document.original_filename,
            )
            text_chunks = self.chunker.split(parsed_document)

            if not text_chunks:
                raise ValueError("Document does not contain extractable text.")

            db_chunks = [
                DocumentChunk(
                    id=uuid.uuid4(),
                    document_id=document.id,
                    user_id=user_id,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                    content_hash=chunk.content_hash,
                    token_count=chunk.token_count,
                    char_start=chunk.char_start,
                    char_end=chunk.char_end,
                    page_start=chunk.page_start,
                    page_end=chunk.page_end,
                    embedding_model=settings.embedding_model,
                    metadata_={"source_filename": document.original_filename},
                )
                for chunk in text_chunks
            ]

            db.add_all(db_chunks)
            db.flush()

            vector_refs = self.vector_search.index_chunks(document, db_chunks)
            refs_by_chunk_id = {vector_ref.chunk_id: vector_ref for vector_ref in vector_refs}

            for chunk in db_chunks:
                vector_ref = refs_by_chunk_id.get(chunk.id)
                if vector_ref:
                    chunk.vector_store = vector_ref.vector_store
                    chunk.vector_collection = vector_ref.vector_collection
                    chunk.vector_id = vector_ref.vector_id

            document.status = "ready"
            document.page_count = parsed_document.page_count
            document.word_count = len(re.findall(r"\S+", parsed_document.text))
            document.summary = document_summary_service.generate_summary(text_chunks, parsed_document.text)
            document.processed_at = datetime.now(UTC)
            document.error_message = None

            db.commit()
            db.refresh(document)

            return self._to_document_read(db, document)
        except Exception as exc:
            db.rollback()
            document.status = "failed"
            document.error_message = str(exc)
            db.add(document)
            db.commit()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to process document: {exc}",
            ) from exc

    def get_documents(self, db: Session, user_id: uuid.UUID) -> list[DocumentRead]:
        self._ensure_user_exists(db, user_id)
        documents = db.scalars(
            select(UploadedDocument)
            .where(UploadedDocument.user_id == user_id)
            .order_by(UploadedDocument.created_at.desc())
        ).all()

        return [self._to_document_read(db, document) for document in documents]

    def delete_document(
        self,
        db: Session,
        document_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> DocumentDeleteResponse:
        document = db.scalar(
            select(UploadedDocument).where(
                UploadedDocument.id == document_id,
                UploadedDocument.user_id == user_id,
            )
        )

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found.",
            )

        deleted_document_id = document.id
        storage_path = document.storage_path
        chunks = db.scalars(
            select(DocumentChunk).where(
                DocumentChunk.document_id == deleted_document_id,
                DocumentChunk.user_id == user_id,
            )
        ).all()

        try:
            db.execute(
                delete(DocumentChunk).where(
                    DocumentChunk.document_id == deleted_document_id,
                    DocumentChunk.user_id == user_id,
                )
            )
            db.delete(document)
            db.commit()
        except Exception as exc:
            db.rollback()
            logger.exception("Failed to delete document document_id=%s user_id=%s", document_id, user_id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete document.",
            ) from exc

        self.vector_search.delete_document_vectors(deleted_document_id, chunks)
        self._delete_storage_file(storage_path)

        return DocumentDeleteResponse(
            message="Document deleted successfully",
            document_id=deleted_document_id,
        )

    def ask_document(
        self,
        db: Session,
        document_id: uuid.UUID,
        user_id: uuid.UUID,
        question: str,
        top_k: int,
    ) -> DocumentAskResponse:
        document = db.scalar(
            select(UploadedDocument).where(
                UploadedDocument.id == document_id,
                UploadedDocument.user_id == user_id,
            )
        )

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found.",
            )

        if document.status != "ready":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Document is not ready for QA. Current status: {document.status}.",
            )

        effective_top_k = max(1, min(top_k or 4, 10))
        hits = self.vector_search.search(db, document_id, question, effective_top_k)
        self._log_selected_hits(document_id=document.id, question=question, hits=hits)

        answer = self.answer_service.generate_answer(question, hits)
        citations = [self._to_citation(hit) for hit in hits]

        return DocumentAskResponse(
            document_id=document.id,
            question=question,
            answer=answer,
            citations=citations,
            used_chunks=len(hits),
            model_provider=settings.llm_provider,
            model_name=settings.llm_model,
        )

    def _delete_storage_file(self, storage_path: str | None) -> None:
        if not storage_path:
            return

        try:
            Path(storage_path).unlink(missing_ok=True)
        except Exception:
            logger.warning("Unable to delete document file at %s", storage_path, exc_info=True)

    def _ensure_user_exists(self, db: Session, user_id: uuid.UUID) -> None:
        if not db.get(User, user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

    def _validate_upload(self, file: UploadFile) -> None:
        filename = file.filename or ""
        suffix = Path(filename).suffix.lower()

        if suffix not in FileParser.supported_extensions and file.content_type not in FileParser.supported_mime_types:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=UNSUPPORTED_FILE_MESSAGE,
            )

    async def _save_upload(
        self,
        file: UploadFile,
        user_id: uuid.UUID,
        document_id: uuid.UUID,
    ) -> tuple[Path, int]:
        upload_dir = Path(settings.upload_dir) / str(user_id)
        upload_dir.mkdir(parents=True, exist_ok=True)

        filename = self._safe_filename(file.filename or "uploaded-document")
        storage_path = upload_dir / f"{document_id}_{filename}"
        content = await file.read()
        storage_path.write_bytes(content)

        return storage_path, len(content)

    def _to_document_read(self, db: Session, document: UploadedDocument) -> DocumentRead:
        chunks_count = db.scalar(
            select(func.count(DocumentChunk.id)).where(DocumentChunk.document_id == document.id)
        )
        return DocumentRead.model_validate(document).model_copy(
            update={"chunks_count": int(chunks_count or 0)}
        )

    def _to_citation(self, hit: SearchHit) -> DocumentCitation:
        excerpt = hit.chunk.content.strip()
        if len(excerpt) > 420:
            excerpt = f"{excerpt[:420].strip()}..."

        return DocumentCitation(
            chunk_id=hit.chunk.id,
            page_start=hit.chunk.page_start,
            page_end=hit.chunk.page_end,
            score=round(hit.score, 4),
            excerpt=excerpt,
            vector_id=hit.chunk.vector_id,
        )

    def _log_selected_hits(self, *, document_id: uuid.UUID, question: str, hits: list[SearchHit]) -> None:
        logger.info(
            "Document QA selected context document_id=%s question=%r selected_chunk_ids=%s scores=%s provider=%s model=%s",
            document_id,
            question,
            [str(hit.chunk.id) for hit in hits],
            [round(hit.score, 4) for hit in hits],
            settings.llm_provider,
            settings.llm_model,
        )


    def _safe_filename(self, filename: str) -> str:
        sanitized = re.sub(r"[^a-zA-Z0-9._-]+", "-", filename).strip("-")
        return sanitized or "uploaded-document"

    def _title_from_filename(self, filename: str) -> str:
        return Path(filename).stem.replace("-", " ").replace("_", " ").strip().title()


document_service = DocumentService()






