"""Command-line interface for QuoteSearch Engine."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

try:
    from . import crawler, indexer, search, storage
except ImportError:  # pragma: no cover - supports python src/main.py
    import crawler
    import indexer
    import search
    import storage


def build_command(index_file: Path) -> int:
    pages = crawler.crawl_site(crawler.BASE_URL)
    if not pages:
        print("No pages were crawled. Index was not created.")
        return 1

    index_data = indexer.build_index(pages, base_url=crawler.BASE_URL)
    saved_path = storage.save_index(index_data, index_file)
    meta = index_data["meta"]
    print(
        f"Built index for {meta['page_count']} pages with "
        f"{meta['unique_terms']} unique terms."
    )
    print(f"Saved compiled index to {saved_path}.")
    return 0


def load_command(index_file: Path) -> int:
    index_data = storage.load_index(index_file)
    meta = index_data["meta"]
    print(f"Loaded index from {index_file}.")
    print(
        f"Pages: {meta.get('page_count', 0)} | "
        f"Unique terms: {meta.get('unique_terms', 0)} | "
        f"Total tokens: {meta.get('total_tokens', 0)}"
    )
    return 0


def print_command(index_file: Path, term: str) -> int:
    index_data = storage.load_index(index_file)
    print(search.format_term_entry(index_data, term))
    return 0


def find_command(index_file: Path, query_parts: list[str]) -> int:
    query = " ".join(query_parts)
    if not query.strip():
        print("No searchable terms were provided. Usage: find <word or phrase>")
        return 1

    index_data = storage.load_index(index_file)
    print(search.format_search_results(index_data, query))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="quotesearch",
        description="Crawl quotes.toscrape.com and search a compiled inverted index.",
    )
    parser.add_argument(
        "--index-file",
        default=storage.DEFAULT_INDEX_PATH,
        type=Path,
        help="Path to the compiled index file. Defaults to data/index.json.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("build", help="Crawl the target site and save a compiled index.")
    subparsers.add_parser("load", help="Load an existing compiled index and print a summary.")

    print_parser = subparsers.add_parser("print", help="Print the inverted index for one term.")
    print_parser.add_argument("term", help="Term to inspect in the inverted index.")

    find_parser = subparsers.add_parser("find", help="Search for one or more terms.")
    find_parser.add_argument("query", nargs="*", help="Search query terms.")
    return parser


def run(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "build":
            return build_command(args.index_file)
        if args.command == "load":
            return load_command(args.index_file)
        if args.command == "print":
            return print_command(args.index_file, args.term)
        if args.command == "find":
            return find_command(args.index_file, args.query)
    except storage.IndexStorageError as exc:
        print(f"Error: {exc}")
        return 1

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(run())

