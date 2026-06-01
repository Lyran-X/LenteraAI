import hashlib
import re
from dataclasses import dataclass

from app.rag.file_parser import PageText, ParsedDocument


@dataclass(frozen=True)
class TextChunk:
    chunk_index: int
    content: str
    content_hash: str
    token_count: int
    char_start: int
    char_end: int
    page_start: int | None
    page_end: int | None


class TextChunker:
    def __init__(self, max_chars: int = 1200, overlap_chars: int = 180) -> None:
        self.max_chars = max_chars
        self.overlap_chars = overlap_chars

    def split(self, parsed_document: ParsedDocument) -> list[TextChunk]:
        text = re.sub(r"\n{3,}", "\n\n", parsed_document.text).strip()

        if not text:
            return []

        chunks: list[TextChunk] = []
        start = 0

        while start < len(text):
            end = min(start + self.max_chars, len(text))
            split_at = self._find_natural_break(text, start, end)
            content = text[start:split_at].strip()

            if content:
                page_start, page_end = self._page_range_for_offsets(
                    parsed_document.pages,
                    start,
                    split_at,
                )
                chunks.append(
                    TextChunk(
                        chunk_index=len(chunks),
                        content=content,
                        content_hash=hashlib.sha256(content.encode("utf-8")).hexdigest(),
                        token_count=len(re.findall(r"\S+", content)),
                        char_start=start,
                        char_end=split_at,
                        page_start=page_start,
                        page_end=page_end,
                    )
                )

            if split_at >= len(text):
                break

            next_start = max(split_at - self.overlap_chars, start + 1)
            start = next_start

        return chunks

    def _find_natural_break(self, text: str, start: int, end: int) -> int:
        if end >= len(text):
            return len(text)

        window = text[start:end]
        for separator in ("\n\n", ". ", "\n", " "):
            index = window.rfind(separator)
            if index >= int(self.max_chars * 0.55):
                return start + index + len(separator)

        return end

    def _page_range_for_offsets(
        self,
        pages: list[PageText],
        start: int,
        end: int,
    ) -> tuple[int | None, int | None]:
        matching_pages = [
            page.page_number
            for page in pages
            if page.char_start <= end and page.char_end >= start
        ]

        if not matching_pages:
            return None, None

        return min(matching_pages), max(matching_pages)
