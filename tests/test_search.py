from __future__ import annotations

from crawler import Page
import indexer
import search


def sample_index():
    return indexer.build_index(
        [
            Page(
                url="https://quotes.toscrape.com/",
                title="Page 1",
                text="Good friends bring good ideas.",
                status_code=200,
            ),
            Page(
                url="https://quotes.toscrape.com/page/2/",
                title="Page 2",
                text="Good ideas matter more than distant friends.",
                status_code=200,
            ),
        ],
        base_url="https://quotes.toscrape.com/",
    )


def test_search_returns_case_insensitive_single_word_results_ranked_by_frequency():
    results = search.search(sample_index(), "GOOD")

    assert [result["url"] for result in results] == [
        "https://quotes.toscrape.com/",
        "https://quotes.toscrape.com/page/2/",
    ]
    assert results[0]["terms"]["good"]["frequency"] == 2


def test_search_handles_multi_word_query_and_phrase_boost():
    results = search.search(sample_index(), "good friends")

    assert len(results) == 2
    assert results[0]["url"] == "https://quotes.toscrape.com/"
    assert results[0]["phrase_match"] is True
    assert results[1]["phrase_match"] is False


def test_search_returns_empty_for_missing_terms():
    assert search.search(sample_index(), "notfound") == []


def test_search_rejects_empty_or_special_character_query():
    try:
        search.search(sample_index(), "!!!")
    except ValueError as exc:
        assert "No searchable terms" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_format_print_and_find_messages():
    data = sample_index()

    assert "Document frequency" in search.format_term_entry(data, "good")
    assert "No index entry found" in search.format_term_entry(data, "unknown")
    assert "No searchable term" in search.format_term_entry(data, "!!!")
    assert "Total results: 2" in search.format_search_results(data, "good friends")
    assert "No pages found" in search.format_search_results(data, "unknown")
    assert "No searchable terms" in search.format_search_results(data, "!!!")

