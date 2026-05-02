from __future__ import annotations

from crawler import Page
import main


def test_cli_build_load_print_and_find(tmp_path, monkeypatch, capsys):
    index_file = tmp_path / "index.json"

    def fake_crawl_site(_base_url):
        return [
            Page(
                url="https://quotes.toscrape.com/",
                title="Page 1",
                text="Good friends keep good company.",
                status_code=200,
            )
        ]

    monkeypatch.setattr(main.crawler, "crawl_site", fake_crawl_site)

    assert main.run(["--index-file", str(index_file), "build"]) == 0
    assert index_file.exists()
    assert "Built index for 1 pages" in capsys.readouterr().out

    assert main.run(["--index-file", str(index_file), "load"]) == 0
    assert "Loaded index" in capsys.readouterr().out

    assert main.run(["--index-file", str(index_file), "print", "GOOD"]) == 0
    assert "Index entry for 'good'" in capsys.readouterr().out

    assert main.run(["--index-file", str(index_file), "find", "good", "friends"]) == 0
    assert "Total results: 1" in capsys.readouterr().out


def test_cli_find_empty_query_returns_clear_error(tmp_path, capsys):
    assert main.run(["--index-file", str(tmp_path / "index.json"), "find"]) == 1

    assert "Usage: find <word or phrase>" in capsys.readouterr().out


def test_cli_reports_missing_index_file(tmp_path, capsys):
    assert main.run(["--index-file", str(tmp_path / "missing.json"), "load"]) == 1

    assert "Error: Index file not found" in capsys.readouterr().out
