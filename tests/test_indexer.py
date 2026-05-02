from __future__ import annotations

from crawler import Page
import indexer


def test_tokenize_normalizes_case_and_punctuation():
    assert indexer.tokenize("Good, GOOD! friend's @value") == [
        "good",
        "good",
        "friend's",
        "value",
    ]


def test_build_index_records_frequency_positions_and_page_metadata():
    pages = [
        Page(
            url="https://quotes.toscrape.com/",
            title="Page 1",
            text="Good friends need good words.",
            status_code=200,
        ),
        Page(
            url="https://quotes.toscrape.com/page/2/",
            title="Page 2",
            text="Words matter.",
            status_code=200,
        ),
    ]

    index_data = indexer.build_index(pages, base_url="https://quotes.toscrape.com/")

    good_entry = index_data["index"]["good"]
    assert good_entry["doc_freq"] == 1
    assert good_entry["postings"]["https://quotes.toscrape.com/"]["frequency"] == 2
    assert good_entry["postings"]["https://quotes.toscrape.com/"]["positions"] == [0, 3]
    assert index_data["pages"]["https://quotes.toscrape.com/"]["word_count"] == 5
    assert index_data["meta"]["page_count"] == 2
    assert index_data["meta"]["unique_terms"] == 5

