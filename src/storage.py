"""Storage helpers for compiled search indexes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_INDEX_PATH = Path("data/index.json")


class IndexStorageError(Exception):
    """Raised when an index file cannot be saved or loaded safely."""


def save_index(index_data: dict[str, Any], path: str | Path = DEFAULT_INDEX_PATH) -> Path:
    """Save the compiled index as readable JSON."""

    index_path = Path(path)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        index_path.write_text(
            json.dumps(index_data, ensure_ascii=True, indent=2, sort_keys=True),
            encoding="utf-8",
        )
    except OSError as exc:
        raise IndexStorageError(f"Could not save index to {index_path}: {exc}") from exc
    return index_path


def load_index(path: str | Path = DEFAULT_INDEX_PATH) -> dict[str, Any]:
    """Load and validate a compiled index file."""

    index_path = Path(path)
    if not index_path.exists():
        raise IndexStorageError(
            f"Index file not found at {index_path}. Run 'build' before 'load', 'print', or 'find'."
        )

    try:
        index_data = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise IndexStorageError(f"Index file at {index_path} is not valid JSON: {exc}") from exc
    except OSError as exc:
        raise IndexStorageError(f"Could not read index from {index_path}: {exc}") from exc

    if not isinstance(index_data, dict) or "meta" not in index_data or "index" not in index_data:
        raise IndexStorageError(f"Index file at {index_path} has an invalid structure.")

    return index_data

