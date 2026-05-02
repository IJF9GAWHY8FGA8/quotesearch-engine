"""Inverted index construction for crawled quote pages."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
import re
from typing import Any, Iterable


TOKEN_RE = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?")
INDEX_VERSION = 1


def tokenize(text: str) -> list[str]:
    """Tokenize text into lower-case searchable terms."""

    return TOKEN_RE.findall(text.lower())


def _read_page_field(page: Any, field: str, default: Any = "") -> Any:
    if isinstance(page, dict):
        return page.get(field, default)
    return getattr(page, field, default)


def build_index(pages: Iterable[Any], *, base_url: str) -> dict[str, Any]:
    """Build a JSON-serializable inverted index from crawled pages."""

    index: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"doc_freq": 0, "postings": {}}
    )
    page_records: dict[str, dict[str, Any]] = {}
    page_count = 0
    total_tokens = 0

    for page in pages:
        url = str(_read_page_field(page, "url"))
        title = str(_read_page_field(page, "title"))
        text = str(_read_page_field(page, "text"))
        tokens = tokenize(text)
        page_count += 1
        total_tokens += len(tokens)
        page_records[url] = {"title": title, "word_count": len(tokens)}

        positions_by_term: dict[str, list[int]] = defaultdict(list)
        for position, token in enumerate(tokens):
            positions_by_term[token].append(position)

        for term, positions in positions_by_term.items():
            index[term]["postings"][url] = {
                "frequency": len(positions),
                "positions": positions,
            }

    for term_data in index.values():
        term_data["doc_freq"] = len(term_data["postings"])

    return {
        "meta": {
            "version": INDEX_VERSION,
            "base_url": base_url,
            "built_at": datetime.now(timezone.utc).isoformat(),
            "page_count": page_count,
            "total_tokens": total_tokens,
            "unique_terms": len(index),
        },
        "pages": page_records,
        "index": dict(sorted(index.items())),
    }

