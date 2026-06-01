import logging
import os
import re
import uuid
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.document import DocumentChunk, UploadedDocument
from app.rag.embedding_service import EmbeddingService


logger = logging.getLogger(__name__)


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "what",
    "with",
    "apa",
    "adalah",
    "atau",
    "bagaimana",
    "dalam",
    "dan",
    "dari",
    "di",
    "itu",
    "jelaskan",
    "ke",
    "pada",
    "tentang",
    "untuk",
    "yang",
}

DEFINITION_MARKERS = {
    "adalah",
    "merupakan",
    "didefinisikan",
    "pengertian",
    "definition",
    "defined",
    "refers",
    "means",
    "is a",
    "is an",
}

DEFINITION_QUESTION_TERMS = {"apa", "what", "define", "definition", "pengertian"}


@dataclass(frozen=True)
class VectorReference:
    chunk_id: uuid.UUID
    vector_store: str
    vector_collection: str | None
    vector_id: str


@dataclass(frozen=True)
class SearchHit:
    chunk: DocumentChunk
    score: float


class VectorSearchService:
    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.collection = None
        self.backend_name = "lexical_fallback"
        self.persist_dir = self._resolve_chroma_persist_dir()
        self._initialize_chroma()

    def _resolve_chroma_persist_dir(self) -> Path:
        configured_path = settings.chroma_persist_dir or settings.vector_db_path or "./storage/chroma"
        persist_dir = Path(configured_path).expanduser()
        if not persist_dir.is_absolute():
            persist_dir = Path.cwd() / persist_dir
        return persist_dir.resolve()

    def _initialize_chroma(self) -> None:
        vector_store = (settings.vector_store or "chroma").strip().lower()
        if vector_store != "chroma":
            logger.info(
                '[RAG] Chroma vector store disabled chroma_enabled=False vector_store=%s retrieval_mode="lexical_fallback"',
                vector_store,
            )
            return

        os.environ["ANONYMIZED_TELEMETRY"] = "False"

        try:
            import chromadb
            from chromadb.config import Settings as ChromaSettings
        except ImportError:
            logger.warning(
                '[RAG] Chroma vector store disabled chroma_enabled=False reason="chromadb_not_installed" retrieval_mode="lexical_fallback"'
            )
            return

        try:
            self.persist_dir.mkdir(parents=True, exist_ok=True)
            client = chromadb.PersistentClient(
                path=str(self.persist_dir),
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    chroma_product_telemetry_impl="app.rag.chroma_telemetry.NoOpChromaTelemetry",
                    chroma_telemetry_impl="app.rag.chroma_telemetry.NoOpChromaTelemetry",
                ),
            )
            self.collection = client.get_or_create_collection(
                name=settings.vector_collection,
                metadata={"hnsw:space": "cosine"},
            )
            self.backend_name = "chroma"
            logger.info(
                '[RAG] Chroma vector store enabled chroma_enabled=True retrieval_mode="chroma" vector_store="chroma" chroma_persist_dir=%s collection=%s',
                self.persist_dir,
                settings.vector_collection,
            )
        except Exception as exc:
            self.collection = None
            self.backend_name = "lexical_fallback"
            logger.warning(
                '[RAG] Chroma vector store disabled chroma_enabled=False reason="init_failed" retrieval_mode="lexical_fallback" chroma_persist_dir=%s collection=%s error_type=%s',
                self.persist_dir,
                settings.vector_collection,
                type(exc).__name__,
                exc_info=True,
            )

    def index_chunks(
        self,
        document: UploadedDocument,
        chunks: list[DocumentChunk],
    ) -> list[VectorReference]:
        if not chunks:
            logger.info(
                '[RAG] Document vector indexing skipped document_id=%s retrieval_mode="%s" indexed_chunks=0',
                document.id,
                self.backend_name,
            )
            return []

        if self.collection is None:
            logger.info(
                '[RAG] Document vector indexing skipped document_id=%s chroma_enabled=False retrieval_mode="lexical_fallback" indexed_chunks=0 reason="chroma_unavailable"',
                document.id,
            )
            return self._fallback_vector_refs(chunks)

        try:
            embeddings = self.embedding_service.embed_texts([chunk.content for chunk in chunks])
            ids = [str(chunk.id) for chunk in chunks]
            metadatas = [
                {
                    "document_id": str(document.id),
                    "user_id": str(document.user_id),
                    "chunk_id": str(chunk.id),
                    "chunk_index": chunk.chunk_index,
                    "page_start": chunk.page_start or -1,
                    "page_end": chunk.page_end or -1,
                }
                for chunk in chunks
            ]

            self.collection.upsert(
                ids=ids,
                documents=[chunk.content for chunk in chunks],
                embeddings=embeddings,
                metadatas=metadatas,
            )
        except Exception as exc:
            logger.warning(
                '[RAG] Document vector indexing failed document_id=%s chroma_enabled=False retrieval_mode="lexical_fallback" chunks_attempted=%s collection=%s error_type=%s',
                document.id,
                len(chunks),
                settings.vector_collection,
                type(exc).__name__,
                exc_info=True,
            )
            return self._fallback_vector_refs(chunks)

        logger.info(
            '[RAG] Chroma indexing completed document_id=%s chroma_enabled=True retrieval_mode="chroma" vector_store="chroma" chroma_persist_dir=%s collection=%s indexed_chunks=%s',
            document.id,
            self.persist_dir,
            settings.vector_collection,
            len(chunks),
        )

        return [
            VectorReference(
                chunk_id=chunk.id,
                vector_store="chroma",
                vector_collection=settings.vector_collection,
                vector_id=str(chunk.id),
            )
            for chunk in chunks
        ]

    def search(
        self,
        db: Session,
        document_id: uuid.UUID,
        query: str,
        top_k: int,
    ) -> list[SearchHit]:
        requested_top_k = max(1, min(top_k or 4, 10))
        candidate_limit = max(requested_top_k * 4, 12)

        retrieval_mode = "lexical_fallback"
        candidates: list[SearchHit] = []

        if self.collection is not None:
            if self._document_needs_chroma_index(db, document_id):
                self._reindex_document_chunks(db, document_id, reason="missing_chroma_metadata")

            candidates = self._search_chroma(db, document_id, query, candidate_limit)

            if not candidates and self._reindex_document_chunks(db, document_id, reason="empty_chroma_results"):
                candidates = self._search_chroma(db, document_id, query, candidate_limit)

            if candidates:
                retrieval_mode = "chroma"

        if not candidates:
            candidates = self._search_postgres_lexical(db, document_id, query, candidate_limit)

        hits = self._rerank_hits(query, candidates, requested_top_k)
        logger.info(
            '[RAG] Document retrieval completed document_id=%s retrieval_mode="%s" collection=%s requested_top_k=%s returned_chunks=%s',
            document_id,
            retrieval_mode,
            settings.vector_collection if retrieval_mode == "chroma" else None,
            requested_top_k,
            len(hits),
        )
        return hits

    def delete_document_vectors(self, document_id: uuid.UUID, chunks: list[DocumentChunk] | None = None) -> None:
        if self.collection is None:
            logger.info(
                '[RAG] Document vector delete skipped document_id=%s retrieval_mode="lexical_fallback" reason="chroma_unavailable"',
                document_id,
            )
            return

        try:
            vector_ids = [chunk.vector_id for chunk in chunks or [] if chunk.vector_id]
            if vector_ids:
                self.collection.delete(ids=vector_ids)
                logger.info(
                    '[RAG] Document vectors deleted document_id=%s retrieval_mode="chroma" collection=%s vector_count=%s',
                    document_id,
                    settings.vector_collection,
                    len(vector_ids),
                )
                return

            self.collection.delete(where={"document_id": str(document_id)})
            logger.info(
                '[RAG] Document vectors deleted document_id=%s retrieval_mode="chroma" collection=%s delete_filter=document_id',
                document_id,
                settings.vector_collection,
            )
        except Exception:
            logger.warning(
                '[RAG] Document vector delete failed document_id=%s collection=%s',
                document_id,
                settings.vector_collection,
                exc_info=True,
            )

    def _fallback_vector_refs(self, chunks: list[DocumentChunk]) -> list[VectorReference]:
        return [
            VectorReference(
                chunk_id=chunk.id,
                vector_store="lexical_fallback",
                vector_collection=None,
                vector_id=str(chunk.id),
            )
            for chunk in chunks
        ]

    def _document_needs_chroma_index(self, db: Session, document_id: uuid.UUID) -> bool:
        if self.collection is None:
            return False

        chunks = self._get_document_chunks(db, document_id)
        if not chunks:
            return False

        return any(
            chunk.vector_store != "chroma"
            or chunk.vector_collection != settings.vector_collection
            or not chunk.vector_id
            for chunk in chunks
        )

    def _reindex_document_chunks(self, db: Session, document_id: uuid.UUID, reason: str) -> bool:
        if self.collection is None:
            return False

        document = db.get(UploadedDocument, document_id)
        if not document:
            return False

        chunks = self._get_document_chunks(db, document_id)
        if not chunks:
            logger.info(
                '[RAG] Document reindex skipped document_id=%s retrieval_mode="chroma" reason="no_chunks"',
                document_id,
            )
            return False

        vector_refs = self.index_chunks(document, chunks)
        refs_by_chunk_id = {vector_ref.chunk_id: vector_ref for vector_ref in vector_refs}
        indexed_count = 0

        for chunk in chunks:
            vector_ref = refs_by_chunk_id.get(chunk.id)
            if not vector_ref or vector_ref.vector_store != "chroma":
                continue
            chunk.vector_store = vector_ref.vector_store
            chunk.vector_collection = vector_ref.vector_collection
            chunk.vector_id = vector_ref.vector_id
            indexed_count += 1

        if indexed_count == 0:
            return False

        db.commit()
        logger.info(
            '[RAG] Document chunks reindexed document_id=%s chroma_enabled=True retrieval_mode="chroma" reason=%s collection=%s indexed_chunks=%s',
            document_id,
            reason,
            settings.vector_collection,
            indexed_count,
        )
        return True

    def _get_document_chunks(self, db: Session, document_id: uuid.UUID) -> list[DocumentChunk]:
        return db.scalars(
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index)
        ).all()

    def _search_chroma(
        self,
        db: Session,
        document_id: uuid.UUID,
        query: str,
        top_k: int,
    ) -> list[SearchHit]:
        vector_count = self._count_chroma_document_vectors(document_id)
        if vector_count == 0:
            logger.info(
                '[RAG] Chroma search skipped document_id=%s retrieval_mode="chroma" reason="no_vectors_for_document" requested_top_k=%s returned_chunks=0',
                document_id,
                top_k,
            )
            return []

        effective_top_k = min(top_k, vector_count) if vector_count is not None else top_k
        effective_top_k = max(1, effective_top_k)

        try:
            result = self.collection.query(
                query_embeddings=[self.embedding_service.embed_text(query)],
                n_results=effective_top_k,
                where={"document_id": str(document_id)},
                include=["distances"],
            )
        except Exception as exc:
            logger.warning(
                '[RAG] Chroma search failed document_id=%s retrieval_mode="lexical_fallback" collection=%s requested_top_k=%s effective_top_k=%s error_type=%s',
                document_id,
                settings.vector_collection,
                top_k,
                effective_top_k,
                type(exc).__name__,
                exc_info=True,
            )
            return []

        ids = [uuid.UUID(value) for value in (result.get("ids") or [[]])[0]]
        distances = (result.get("distances") or [[]])[0]

        if not ids:
            return []

        chunks = db.scalars(select(DocumentChunk).where(DocumentChunk.id.in_(ids))).all()
        chunks_by_id = {chunk.id: chunk for chunk in chunks}

        ordered_hits: list[SearchHit] = []
        for index, chunk_id in enumerate(ids):
            chunk = chunks_by_id.get(chunk_id)
            if not chunk:
                continue

            distance = distances[index] if index < len(distances) else 1.0
            score = max(0.0, min(1.0, 1.0 - float(distance)))
            ordered_hits.append(SearchHit(chunk=chunk, score=score))

        logger.info(
            '[RAG] Chroma search completed document_id=%s retrieval_mode="chroma" collection=%s requested_top_k=%s effective_top_k=%s returned_chunks=%s document_vector_count=%s',
            document_id,
            settings.vector_collection,
            top_k,
            effective_top_k,
            len(ordered_hits),
            vector_count,
        )
        return ordered_hits

    def _count_chroma_document_vectors(self, document_id: uuid.UUID) -> int | None:
        if self.collection is None:
            return None

        try:
            result = self.collection.get(
                where={"document_id": str(document_id)},
                include=["metadatas"],
            )
        except Exception as exc:
            logger.warning(
                '[RAG] Chroma vector count failed document_id=%s collection=%s error_type=%s',
                document_id,
                settings.vector_collection,
                type(exc).__name__,
                exc_info=True,
            )
            return None

        return len(result.get("ids") or [])

    def _search_postgres_lexical(
        self,
        db: Session,
        document_id: uuid.UUID,
        query: str,
        top_k: int,
    ) -> list[SearchHit]:
        chunks = self._get_document_chunks(db, document_id)

        query_terms = self._important_terms(query)
        scored_hits: list[SearchHit] = []

        for chunk in chunks:
            lexical_score = self._keyword_overlap_score(query_terms, chunk.content)
            scored_hits.append(SearchHit(chunk=chunk, score=lexical_score))

        scored_hits.sort(key=lambda hit: hit.score, reverse=True)
        hits = scored_hits[:top_k]
        logger.info(
            '[RAG] Lexical fallback search completed document_id=%s retrieval_mode="lexical_fallback" candidate_chunks=%s',
            document_id,
            len(hits),
        )
        return hits

    def _rerank_hits(self, query: str, hits: list[SearchHit], top_k: int) -> list[SearchHit]:
        if not hits:
            return []

        query_terms = self._important_terms(query)
        phrases = self._important_phrases(query)
        wants_definition = bool(set(self._tokens(query)).intersection(DEFINITION_QUESTION_TERMS))

        reranked: list[SearchHit] = []
        for hit in hits:
            text = hit.chunk.content
            keyword_score = self._keyword_overlap_score(query_terms, text)
            phrase_score = self._phrase_score(phrases, text)
            definition_score = self._definition_score(text, wants_definition, phrases)

            combined_score = min(
                1.0,
                (hit.score * 0.50) + (keyword_score * 0.32) + (phrase_score * 0.13) + definition_score,
            )
            reranked.append(SearchHit(chunk=hit.chunk, score=combined_score))

        reranked.sort(key=lambda hit: (hit.score, -hit.chunk.chunk_index), reverse=True)
        return reranked[:top_k]

    def _important_terms(self, text: str) -> list[str]:
        return [token for token in self._tokens(text) if token not in STOPWORDS and len(token) > 1]

    def _important_phrases(self, text: str) -> list[str]:
        terms = self._important_terms(text)
        phrases: list[str] = []

        for size in (4, 3, 2):
            for index in range(0, max(len(terms) - size + 1, 0)):
                phrase = " ".join(terms[index : index + size])
                if phrase not in phrases:
                    phrases.append(phrase)

        return phrases[:8]

    def _tokens(self, text: str) -> list[str]:
        return re.findall(r"[a-zA-Z0-9_]+", text.lower().replace("_", " "))

    def _keyword_overlap_score(self, query_terms: list[str], chunk_text: str) -> float:
        if not query_terms:
            return 0.0

        chunk_terms = set(self._tokens(chunk_text))
        if not chunk_terms:
            return 0.0

        total_weight = 0.0
        matched_weight = 0.0
        for term in query_terms:
            weight = 1.4 if len(term) > 3 else 1.0
            total_weight += weight
            if term in chunk_terms:
                matched_weight += weight

        return matched_weight / max(total_weight, 1.0)

    def _phrase_score(self, phrases: list[str], chunk_text: str) -> float:
        if not phrases:
            return 0.0

        normalized_chunk = re.sub(r"\s+", " ", chunk_text.lower())
        score = 0.0
        for phrase in phrases:
            if phrase in normalized_chunk:
                score += min(0.34, 0.10 + (0.04 * len(phrase.split())))

        return min(score, 1.0)

    def _definition_score(self, chunk_text: str, wants_definition: bool, phrases: list[str]) -> float:
        if not wants_definition:
            return 0.0

        normalized_chunk = re.sub(r"\s+", " ", chunk_text.lower())
        has_marker = any(marker in normalized_chunk for marker in DEFINITION_MARKERS)
        has_phrase = any(phrase in normalized_chunk for phrase in phrases) if phrases else True

        if has_marker and has_phrase:
            return 0.12
        if has_marker:
            return 0.06
        return 0.0
