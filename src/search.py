"""Search and formatting helpers for the quote inverted index."""

from __future__ import annotations

from typing import Any

try:
    from .indexer import tokenize
except ImportError:  # pragma: no cover - supports python src/main.py
    from indexer import tokenize


def normalize_query(query: str) -> list[str]:
    """Normalize a user query into searchable terms."""

    return tokenize(query)


def get_term_entry(index_data: dict[str, Any], term: str) -> tuple[str, dict[str, Any] | None]:
    """Return the normalized term and its index entry."""

    terms = normalize_query(term)
    if not terms:
        return "", None
    normalized = terms[0]
    return normalized, index_data.get("index", {}).get(normalized)


def has_phrase_match(term_positions: list[list[int]]) -> bool:
    """Return True when query terms appear in consecutive positions."""

    if len(term_positions) <= 1:
        return False

    remaining = [set(positions) for positions in term_positions[1:]]
    for start in term_positions[0]:
        if all((start + offset + 1) in positions for offset, positions in enumerate(remaining)):
            return True
    return False


def search(index_data: dict[str, Any], query: str) -> list[dict[str, Any]]:
    """Search for pages containing all normalized query terms."""

    terms = normalize_query(query)
    if not terms:
        raise ValueError("No searchable terms were provided.")

    inverted = index_data.get("index", {})
    missing_terms = [term for term in terms if term not in inverted]
    if missing_terms:
        return []

    matching_urls = set(inverted[terms[0]]["postings"].keys())
    for term in terms[1:]:
        matching_urls &= set(inverted[term]["postings"].keys())

    pages = index_data.get("pages", {})
    results: list[dict[str, Any]] = []
    for url in matching_urls:
        term_details = {
            term: inverted[term]["postings"][url]
            for term in terms
        }
        positions = [term_details[term]["positions"] for term in terms]
        phrase_match = has_phrase_match(positions)
        frequency_score = sum(term_details[term]["frequency"] for term in terms)
        score = frequency_score + (10 if phrase_match else 0)
        results.append(
            {
                "url": url,
                "title": pages.get(url, {}).get("title", ""),
                "score": score,
                "phrase_match": phrase_match,
                "terms": {
                    term: {
                        "frequency": term_details[term]["frequency"],
                        "positions": term_details[term]["positions"],
                    }
                    for term in terms
                },
            }
        )

    return sorted(
        results,
        key=lambda item: (
            not item["phrase_match"],
            -item["score"],
            item["url"],
        ),
    )


def format_term_entry(index_data: dict[str, Any], term: str) -> str:
    """Format a single term posting list for the CLI print command."""

    normalized, entry = get_term_entry(index_data, term)
    if not normalized:
        return "No searchable term found in input."
    if not entry:
        return f"No index entry found for '{normalized}'."

    lines = [
        f"Index entry for '{normalized}'",
        f"Document frequency: {entry['doc_freq']}",
    ]
    for url, posting in sorted(entry["postings"].items()):
        lines.append(
            f"- {url} | frequency={posting['frequency']} | positions={posting['positions']}"
        )
    return "\n".join(lines)


def format_search_results(index_data: dict[str, Any], query: str) -> str:
    """Format ranked search results for the CLI find command."""

    terms = normalize_query(query)
    if not terms:
        return "No searchable terms were provided."

    results = search(index_data, query)
    if not results:
        return f"No pages found for query: {' '.join(terms)}"

    lines = [f"Results for query: {' '.join(terms)}", f"Total results: {len(results)}"]
    for number, result in enumerate(results, start=1):
        phrase_label = "yes" if result["phrase_match"] else "no"
        term_summary = ", ".join(
            f"{term}={details['frequency']}"
            for term, details in result["terms"].items()
        )
        lines.append(
            f"{number}. {result['url']} | score={result['score']} | "
            f"phrase_match={phrase_label} | {term_summary}"
        )
    return "\n".join(lines)

