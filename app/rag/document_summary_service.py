import logging
import re
from collections import Counter

from app.rag.text_chunker import TextChunk
from app.services.llm_service import llm_service


logger = logging.getLogger(__name__)


SUMMARY_SYSTEM_PROMPT = """
You are EduPath AI Document Summarizer.
Create a concise one-paragraph summary in Indonesian for a student dashboard.
The summary must cover the main idea, the document's core topic or purpose, and important points from across the document.
Do not merely copy the opening paragraph.
Do not include journal metadata, URLs, copyright notes, author names, license text, or publication boilerplate unless they are the actual main point.
Do not use bullet lists, headings, tables, or markdown.
Maximum 4 to 6 sentences and maximum 600 characters.
""".strip()


SUMMARY_USER_PROMPT = """
Buat ringkasan satu paragraf dalam bahasa Indonesia dari isi dokumen berikut. Ringkasan harus mencakup ide pokok utama, tujuan/topik utama, dan poin penting dokumen. Jangan hanya menyalin paragraf awal. Jangan terlalu panjang. Maksimal 4-6 kalimat dan maksimal 600 karakter.

Isi dokumen representatif:
{context}
""".strip()


STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "is", "it", "of", "on", "or", "that", "the", "this", "to", "with",
    "ada", "adalah", "agar", "akan", "atau", "bagian", "dalam", "dan", "dari", "dengan", "di", "ini", "itu", "ke", "pada", "sebagai", "untuk", "yang",
}

METADATA_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"https?://",
        r"\bdoi\b",
        r"\bissn\b",
        r"\bisbn\b",
        r"copyright",
        r"creative\s+commons",
        r"all\s+rights\s+reserved",
        r"license|licence",
        r"received\s*:",
        r"accepted\s*:",
        r"published\s*:",
        r"corresponding\s+author",
        r"\bemail\b|@",
        r"\bvol\.?\s*\d+|\bvolume\b|\bissue\b",
        r"\bjournal\b",
        r"\bproceedings\b",
    )
]


class DocumentSummaryService:
    max_summary_chars = 600
    max_context_chars = 5200

    def generate_summary(self, chunks: list[TextChunk], full_text: str) -> str:
        if not chunks and not full_text.strip():
            return ""

        selected_chunks = self._select_representative_chunks(chunks)
        context = self._build_context(selected_chunks, full_text)

        if context:
            result = llm_service.generate_text_response(
                system_prompt=SUMMARY_SYSTEM_PROMPT,
                user_prompt=SUMMARY_USER_PROMPT.format(context=context),
            )

            logger.info(
                "Document summary LLM result provider=%s model=%s fallback=%s latency_ms=%s",
                result.provider,
                result.model,
                result.metadata.get("fallback", False),
                result.latency_ms,
            )

            if not result.metadata.get("fallback") and not self._is_provider_fallback(result.content):
                summary = self._clean_summary(result.content)
                if summary:
                    return summary

        return self._fallback_summary(selected_chunks, full_text)

    def _select_representative_chunks(self, chunks: list[TextChunk]) -> list[TextChunk]:
        if not chunks:
            return []

        indexes = {0, len(chunks) // 2, len(chunks) - 1}
        keyword_chunks = self._keyword_representative_chunks(chunks, limit=3)
        indexes.update(chunk.chunk_index for chunk in keyword_chunks)

        selected = [chunk for chunk in chunks if chunk.chunk_index in indexes]
        selected.sort(key=lambda chunk: chunk.chunk_index)
        return selected[:7]

    def _keyword_representative_chunks(self, chunks: list[TextChunk], limit: int) -> list[TextChunk]:
        keywords = self._top_keywords("\n".join(chunk.content for chunk in chunks), limit=14)
        if not keywords:
            return []

        scored: list[tuple[float, TextChunk]] = []
        for chunk in chunks:
            text = chunk.content.lower()
            score = sum(text.count(keyword) for keyword in keywords)
            if self._looks_like_metadata(chunk.content):
                score *= 0.35
            scored.append((float(score), chunk))

        scored.sort(key=lambda item: (item[0], -item[1].chunk_index), reverse=True)
        return [chunk for score, chunk in scored if score > 0][:limit]

    def _build_context(self, chunks: list[TextChunk], full_text: str) -> str:
        if chunks:
            blocks = []
            for chunk in chunks:
                excerpt = self._compact_text(chunk.content, 900)
                if excerpt:
                    blocks.append(f"Chunk {chunk.chunk_index + 1}: {excerpt}")
            context = "\n\n".join(blocks)
        else:
            context = self._compact_text(full_text, self.max_context_chars)

        return self._compact_text(context, self.max_context_chars)

    def _fallback_summary(self, chunks: list[TextChunk], full_text: str) -> str:
        source_text = "\n".join(chunk.content for chunk in chunks) if chunks else full_text
        sentences = self._split_sentences(source_text)
        candidates = [sentence for sentence in sentences if self._is_content_sentence(sentence)]

        if not candidates:
            return self._clean_summary(self._compact_text(source_text, self.max_summary_chars))

        keywords = self._top_keywords(" ".join(candidates), limit=16)
        scored: list[tuple[float, int, str]] = []
        for index, sentence in enumerate(candidates):
            normalized = sentence.lower()
            score = sum(normalized.count(keyword) for keyword in keywords)
            if 80 <= len(sentence) <= 240:
                score += 1.5
            if self._looks_like_metadata(sentence):
                score -= 4
            scored.append((float(score), index, sentence))

        selected = sorted(scored, key=lambda item: item[0], reverse=True)[:5]
        selected.sort(key=lambda item: item[1])
        summary = " ".join(sentence for _, _, sentence in selected)
        return self._clean_summary(summary)

    def _clean_summary(self, summary: str) -> str:
        cleaned = re.sub(r"[*_`#>\-]+", " ", summary)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        cleaned = re.sub(r"^(ringkasan|summary)\s*:\s*", "", cleaned, flags=re.IGNORECASE).strip()
        cleaned = self._remove_metadata_sentences(cleaned)
        cleaned = self._limit_sentences(cleaned, max_sentences=6)
        if len(cleaned) > self.max_summary_chars:
            cleaned = cleaned[: self.max_summary_chars].rsplit(" ", 1)[0].strip()
        return cleaned.rstrip(" ,;:-")

    def _remove_metadata_sentences(self, text: str) -> str:
        sentences = self._split_sentences(text)
        content_sentences = [sentence for sentence in sentences if not self._looks_like_metadata(sentence)]
        return " ".join(content_sentences or sentences).strip()

    def _limit_sentences(self, text: str, max_sentences: int) -> str:
        sentences = self._split_sentences(text)
        if not sentences:
            return text.strip()
        return " ".join(sentences[:max_sentences]).strip()

    def _split_sentences(self, text: str) -> list[str]:
        compact = re.sub(r"\s+", " ", text).strip()
        if not compact:
            return []
        return [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", compact) if sentence.strip()]

    def _is_content_sentence(self, sentence: str) -> bool:
        if len(sentence) < 45:
            return False
        if self._looks_like_metadata(sentence):
            return False
        alpha_count = len(re.findall(r"[A-Za-zÀ-ÿ]", sentence))
        return alpha_count >= max(20, int(len(sentence) * 0.45))

    def _looks_like_metadata(self, text: str) -> bool:
        return any(pattern.search(text) for pattern in METADATA_PATTERNS)

    def _top_keywords(self, text: str, limit: int) -> list[str]:
        tokens = [
            token
            for token in re.findall(r"[a-zA-ZÀ-ÿ0-9_]+", text.lower().replace("_", " "))
            if len(token) > 3 and token not in STOPWORDS
        ]
        return [token for token, _ in Counter(tokens).most_common(limit)]

    def _compact_text(self, text: str, limit: int) -> str:
        compact = re.sub(r"\s+", " ", text).strip()
        if len(compact) <= limit:
            return compact
        return compact[:limit].rsplit(" ", 1)[0].strip()

    def _is_provider_fallback(self, content: str) -> bool:
        return content.strip().lower().startswith("ai response fallback")


document_summary_service = DocumentSummaryService()
