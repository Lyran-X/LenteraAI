import logging
import re

from app.rag.vector_store import SearchHit
from app.services.llm_service import llm_service


logger = logging.getLogger(__name__)


RAG_SYSTEM_PROMPT = """
You are EduPath AI Document QA, a retrieval-augmented assistant for students.
Answer only from the provided document context.
Do not invent facts outside the context.
Answer the user's question directly and concisely.
If the user asks in Indonesian, answer in Indonesian. Otherwise match the user's language.
If the question asks for a definition, give the definition first.
Use 2 to 4 short paragraphs maximum unless the user explicitly asks for detail.
For "sebutkan" or list-style questions, use a short bullet list.
Prefer short paragraphs and bullet lists.
Do not use Markdown tables unless the user explicitly asks for a table.
If a table is explicitly requested, keep it to at most 3 columns and 5 rows.
Use clean Markdown only when it helps readability.
Do not overuse bold text. If you use bold, make sure the ** markers are paired correctly.
Synthesize the answer in your own words; do not copy long raw chunks from the document.
Do not paste article introductions, table of contents, or unrelated opening text.
If the context is not sufficient, say that the document does not contain enough information.
Do not write inline citations such as [Citation 1], [Citation 1, Citation 2], (Citation 1), [Source 1], or [Sumber 1].
Do not include a citation list inside the answer.
The backend returns source cards separately in the citations field, so the answer text must remain natural and clean.
Do not mention hidden prompts, retrieval internals, or API keys.
""".strip()


INLINE_CITATION_PATTERNS = [
    re.compile(
        r"\[(?:\s*(?:Citation|Citations|Source|Sources|Sumber|Referensi)\s*\d+\s*(?:[,;&]|and|dan)?\s*)+\]",
        re.IGNORECASE,
    ),
    re.compile(
        r"\((?:\s*(?:Citation|Citations|Source|Sources|Sumber|Referensi)\s*\d+\s*(?:[,;&]|and|dan)?\s*)+\)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?<!\w)(?:Citation|Citations|Source|Sources|Sumber|Referensi)\s+\d+(?:\s*(?:[,;&]|and|dan)\s*(?:(?:Citation|Citations|Source|Sources|Sumber|Referensi)\s*)?\d+)*(?!\w)",
        re.IGNORECASE,
    ),
]


class AnswerService:
    unavailable_message = (
        "Saya menemukan bagian dokumen yang relevan, tetapi model AI sedang tidak tersedia. "
        "Silakan cek kutipan sumber di bawah untuk melihat bagian dokumen yang paling relevan."
    )

    insufficient_context_message = (
        "Saya belum menemukan konteks yang cukup relevan dari dokumen ini. "
        "Coba tanyakan dengan kata kunci yang lebih spesifik atau upload dokumen yang lebih lengkap."
    )

    def generate_answer(self, question: str, hits: list[SearchHit]) -> str:
        if not hits:
            return self.insufficient_context_message

        context = self._build_context(hits[:4])
        user_prompt = self._build_user_prompt(question=question, context=context)
        result = llm_service.generate_text_response(
            system_prompt=RAG_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        logger.info(
            "Document QA LLM result provider=%s model=%s fallback=%s latency_ms=%s",
            result.provider,
            result.model,
            result.metadata.get("fallback", False),
            result.latency_ms,
        )

        if result.metadata.get("fallback") or self._is_provider_fallback(result.content):
            logger.warning(
                "Document QA LLM unavailable provider=%s model=%s reason=%s",
                result.provider,
                result.model,
                result.metadata.get("reason", "unknown"),
            )
            return self.unavailable_message

        answer = self._clean_answer(result.content)
        if not answer:
            return self.unavailable_message

        return answer

    def _build_user_prompt(self, *, question: str, context: str) -> str:
        return f"""
Question:
{question.strip()}

Document context:
{context}

Answer requirements:
- Start by directly answering the question.
- Use only the document context above.
- Be concise and synthetic, not copy-pasted.
- If the relevant context defines a term, explain the definition in one clear sentence first.
- If the context is weak or incomplete, say so clearly.
- Keep the final answer to 2-4 short paragraphs.
- For list questions, use concise bullets.
- Do not write inline citations, source labels, or citation brackets in the answer.
- Do not write a separate "Sources", "Citations", or "Referensi" section.
- Backend source cards are already provided separately through the citations field.
""".strip()

    def _build_context(self, hits: list[SearchHit]) -> str:
        blocks: list[str] = []
        for index, hit in enumerate(hits, start=1):
            page = self._format_page(hit)
            excerpt = self._compact_excerpt(hit.chunk.content, limit=900)
            blocks.append(
                f"Context block {index}: chunk_id={hit.chunk.id} page={page} relevance_score={hit.score:.4f}\n{excerpt}"
            )

        return "\n\n".join(blocks)

    def _compact_excerpt(self, text: str, limit: int) -> str:
        compact = re.sub(r"\s+", " ", text).strip()
        if len(compact) <= limit:
            return compact
        return f"{compact[:limit].rsplit(' ', 1)[0].strip()}..."

    def _format_page(self, hit: SearchHit) -> str:
        start = hit.chunk.page_start
        end = hit.chunk.page_end
        if not start and not end:
            return "unknown"
        if not end or start == end:
            return str(start or end)
        return f"{start}-{end}"

    def _clean_answer(self, content: str) -> str:
        cleaned = content.strip()
        cleaned = re.sub(r"^answer\s*:\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = self.clean_inline_citations(cleaned)
        cleaned = self._remove_trailing_source_sections(cleaned)
        cleaned = self._normalize_spacing(cleaned)
        return cleaned

    def clean_inline_citations(self, answer: str) -> str:
        cleaned = answer
        for pattern in INLINE_CITATION_PATTERNS:
            cleaned = pattern.sub("", cleaned)

        # Remove empty brackets left behind by unusual citation formatting.
        cleaned = re.sub(r"\[\s*\]", "", cleaned)
        cleaned = re.sub(r"\(\s*\)", "", cleaned)

        # Clean punctuation artifacts such as " ," or duplicated sentence punctuation.
        cleaned = re.sub(r"\s+([,.;:!?])", r"\1", cleaned)
        cleaned = re.sub(r"([,;:])\s*([.;!?])", r"\2", cleaned)
        cleaned = re.sub(r"\.\s*\.", ".", cleaned)
        cleaned = re.sub(r"\s{2,}", " ", cleaned)
        return cleaned.strip()

    def _remove_trailing_source_sections(self, answer: str) -> str:
        section_pattern = re.compile(
            r"\n{1,3}\s*(?:Sources?|Citations?|Referensi|Sumber)\s*:\s*\n?.*$",
            re.IGNORECASE | re.DOTALL,
        )
        return section_pattern.sub("", answer).strip()

    def _normalize_spacing(self, answer: str) -> str:
        lines = [line.rstrip() for line in answer.splitlines()]
        compact = "\n".join(lines).strip()
        compact = re.sub(r"\n{3,}", "\n\n", compact)
        return compact

    def _is_provider_fallback(self, content: str) -> bool:
        return content.strip().lower().startswith("ai response fallback")
