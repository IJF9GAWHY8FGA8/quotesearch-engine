from __future__ import annotations

import pytest

import storage


def test_save_and_load_index_round_trip(tmp_path):
    index_data = {
        "meta": {"page_count": 1, "unique_terms": 1},
        "pages": {},
        "index": {"good": {"doc_freq": 0, "postings": {}}},
    }
    index_file = tmp_path / "index.json"

    storage.save_index(index_data, index_file)

    assert storage.load_index(index_file) == index_data


def test_load_index_reports_missing_file(tmp_path):
    with pytest.raises(storage.IndexStorageError, match="Run 'build'"):
        storage.load_index(tmp_path / "missing.json")


def test_load_index_reports_invalid_json(tmp_path):
    index_file = tmp_path / "index.json"
    index_file.write_text("{broken json", encoding="utf-8")

    with pytest.raises(storage.IndexStorageError, match="not valid JSON"):
        storage.load_index(index_file)


def test_load_index_reports_invalid_structure(tmp_path):
    index_file = tmp_path / "index.json"
    index_file.write_text("[]", encoding="utf-8")

    with pytest.raises(storage.IndexStorageError, match="invalid structure"):
        storage.load_index(index_file)

