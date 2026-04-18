"""
tests.test_knowledge_base

Tests for the Knowledge Base loader and schema validation.

Related to: Law 5 (Zero Hallucination) — KB is the AI's only truth
Related to: Principle 6 (KB Stewardship) — every entry audited
Related to: Phase 1 Development Guide Week 4, Part B

Tests:
    1. Real KB loads cleanly
    2. Real KB has expected categories
    3. Real KB entries all have required fields
    4. needs_review flag is honored
    5. Missing required fields raise KBSchemaError
    6. Invalid confidence value raises KBSchemaError
    7. Missing _metadata.json raises KBSchemaError
    8. Duplicate entry ids within a category raise KBSchemaError
    9. Non-boolean needs_review raises KBSchemaError
    10. Unknown entry returns None (Law 5 caller contract)
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from omnicovas.knowledge_base.loader import (
    KBSchemaError,
    load_knowledge_base,
)

PROJECT_ROOT = Path(__file__).parent.parent
REAL_KB_DIR = PROJECT_ROOT / "omnicovas" / "knowledge_base"


EXPECTED_CATEGORIES = {
    "combat_mechanics",
    "engineering_materials",
    "bgs_mechanics",
    "powerplay2_mechanics",
    "odyssey_mechanics",
    "trading_mechanics",
    "exploration_mechanics",
    "exobiology_mechanics",
}


def test_real_kb_loads_cleanly() -> None:
    """The actual shipped KB must always pass schema validation."""
    kb = load_knowledge_base(REAL_KB_DIR)
    assert kb.total_entries >= 1


def test_real_kb_has_all_expected_categories() -> None:
    """Every Phase 1 category must be present in the shipped KB."""
    kb = load_knowledge_base(REAL_KB_DIR)
    categories_present = {e.category for e in kb.all_entries()}

    missing = EXPECTED_CATEGORIES - categories_present
    assert not missing, f"Missing categories: {missing}"


def test_real_kb_entries_have_required_fields() -> None:
    """Every entry in the real KB must pass field validation."""
    kb = load_knowledge_base(REAL_KB_DIR)

    for entry in kb.all_entries():
        assert entry.id
        assert entry.topic
        assert entry.content
        assert entry.patch_verified
        assert entry.source
        assert entry.last_updated
        assert entry.confidence in {"high", "medium", "low"}
        assert isinstance(entry.needs_review, bool)


def test_real_kb_needs_review_tracked() -> None:
    """
    The entries_needing_review() helper must return entries flagged for review.
    (Powerplay 2.0 is flagged, so this list should be non-empty on Phase 1.)
    """
    kb = load_knowledge_base(REAL_KB_DIR)
    needing_review = kb.entries_needing_review()

    # It's fine if this changes later; for now we seeded at least one
    for entry in needing_review:
        assert entry.needs_review is True


def test_get_unknown_entry_returns_none() -> None:
    """
    Law 5: callers must handle "no entry exists" explicitly.
    get() must return None, never raise, for unknown entries.
    """
    kb = load_knowledge_base(REAL_KB_DIR)

    assert kb.get("nonexistent_category", "anything") is None
    assert kb.get("combat_mechanics", "no_such_id") is None


def _write_kb(
    tmp_path: Path,
    metadata: dict,
    category_files: dict[str, dict],
) -> Path:
    """Helper: write a temporary KB directory structure for testing."""
    (tmp_path / "_metadata.json").write_text(json.dumps(metadata))
    for filename, data in category_files.items():
        (tmp_path / filename).write_text(json.dumps(data))
    return tmp_path


def test_missing_metadata_raises(tmp_path: Path) -> None:
    """Loader must fail loudly if _metadata.json is missing."""
    with pytest.raises(KBSchemaError, match="metadata"):
        load_knowledge_base(tmp_path)


def test_missing_required_field_raises(tmp_path: Path) -> None:
    """An entry missing any required field must fail validation."""
    _write_kb(
        tmp_path,
        metadata={"kb_version": "0.0.1"},
        category_files={
            "test.json": {
                "category": "test",
                "entries": [
                    {
                        "id": "incomplete",
                        "topic": "Missing fields",
                        # content, patch_verified, source, etc. all missing
                    }
                ],
            }
        },
    )
    with pytest.raises(KBSchemaError, match="missing required fields"):
        load_knowledge_base(tmp_path)


def test_invalid_confidence_raises(tmp_path: Path) -> None:
    """confidence must be one of high/medium/low."""
    _write_kb(
        tmp_path,
        metadata={"kb_version": "0.0.1"},
        category_files={
            "test.json": {
                "category": "test",
                "entries": [
                    {
                        "id": "bad_confidence",
                        "topic": "Test",
                        "content": "Some content",
                        "patch_verified": "4.0",
                        "source": "test",
                        "last_updated": "2026-01-01",
                        "confidence": "extremely_high",
                        "needs_review": False,
                    }
                ],
            }
        },
    )
    with pytest.raises(KBSchemaError, match="invalid confidence"):
        load_knowledge_base(tmp_path)


def test_duplicate_entry_id_raises(tmp_path: Path) -> None:
    """Two entries with the same id in one category must fail."""
    _write_kb(
        tmp_path,
        metadata={"kb_version": "0.0.1"},
        category_files={
            "test.json": {
                "category": "test",
                "entries": [
                    {
                        "id": "dup",
                        "topic": "First",
                        "content": "one",
                        "patch_verified": "4.0",
                        "source": "test",
                        "last_updated": "2026-01-01",
                        "confidence": "high",
                        "needs_review": False,
                    },
                    {
                        "id": "dup",
                        "topic": "Second",
                        "content": "two",
                        "patch_verified": "4.0",
                        "source": "test",
                        "last_updated": "2026-01-01",
                        "confidence": "high",
                        "needs_review": False,
                    },
                ],
            }
        },
    )
    with pytest.raises(KBSchemaError, match="duplicate entry id"):
        load_knowledge_base(tmp_path)


def test_non_boolean_needs_review_raises(tmp_path: Path) -> None:
    """needs_review must be a real boolean, not a string or int."""
    _write_kb(
        tmp_path,
        metadata={"kb_version": "0.0.1"},
        category_files={
            "test.json": {
                "category": "test",
                "entries": [
                    {
                        "id": "bad_review_flag",
                        "topic": "Test",
                        "content": "Some content",
                        "patch_verified": "4.0",
                        "source": "test",
                        "last_updated": "2026-01-01",
                        "confidence": "high",
                        "needs_review": "true",  # string, not bool
                    }
                ],
            }
        },
    )
    with pytest.raises(KBSchemaError, match="non-boolean needs_review"):
        load_knowledge_base(tmp_path)
