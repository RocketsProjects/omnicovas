"""
tests.test_journal_watcher

Tests for JournalWatcher._find_current_journal() — Phase 3.1.2 journal selection repair.

Root cause being fixed: mtime-based selection chose Journal.2026-04-28 instead of
Journal.2026-04-29 during a live test because Windows can update mtime on older files.

Selection must use the timestamp encoded in the filename, with mtime as fallback only
when filename parsing fails entirely.

Tests:
    1. Newest filename timestamp wins even when an older journal has a newer mtime
    2. Same-day files: later HH:MM:SS wins
    3. Non-journal files are ignored (Status.json, .txt, .bak)
    4. Fallback to mtime when filename parsing fails for all files
    5. Regression: 2026-04-29 beats 2026-04-28 and 2026-04-16 even with bad mtime
"""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from omnicovas.core.journal_watcher import JournalWatcher


async def _noop(line: str) -> None:
    pass


def _make_watcher(journal_path: Path) -> JournalWatcher:
    return JournalWatcher(dispatch_fn=_noop, journal_path=journal_path)


def _touch(path: Path, content: str = "") -> Path:
    path.write_text(content, encoding="utf-8")
    return path


@pytest.mark.asyncio
async def test_newest_filename_wins_over_newer_mtime(tmp_path: Path) -> None:
    """
    An older-dated journal with a more recent mtime must NOT win.
    The journal with the newer filename timestamp must be selected.
    """
    old_journal = _touch(tmp_path / "Journal.2026-04-28T133233.01.log")
    new_journal = _touch(tmp_path / "Journal.2026-04-29T144219.01.log")

    # Give the older file a much newer mtime so a naive mtime-sort would pick it
    future_mtime = time.time() + 3600
    import os

    os.utime(old_journal, (future_mtime, future_mtime))

    watcher = _make_watcher(tmp_path)
    selected = watcher._find_current_journal()

    assert selected is not None
    assert selected.name == new_journal.name


@pytest.mark.asyncio
async def test_same_day_later_timestamp_wins(tmp_path: Path) -> None:
    """Two journals from the same day: the later HHMMSS wins."""
    _touch(tmp_path / "Journal.2026-04-29T100000.01.log")
    later = _touch(tmp_path / "Journal.2026-04-29T144219.01.log")

    watcher = _make_watcher(tmp_path)
    selected = watcher._find_current_journal()

    assert selected is not None
    assert selected.name == later.name


@pytest.mark.asyncio
async def test_non_journal_files_ignored(tmp_path: Path) -> None:
    """Status.json, plain .txt, and .bak files must not be considered."""
    _touch(tmp_path / "Status.json", '{"timestamp":"2026-04-29T14:42:19Z"}')
    _touch(tmp_path / "notes.txt")
    _touch(tmp_path / "Journal.2026-04-29T144219.01.log.bak")
    expected = _touch(tmp_path / "Journal.2026-04-29T144219.01.log")

    watcher = _make_watcher(tmp_path)
    selected = watcher._find_current_journal()

    assert selected is not None
    assert selected.name == expected.name


@pytest.mark.asyncio
async def test_fallback_mtime_when_filename_unparseable(tmp_path: Path) -> None:
    """
    When no filename matches the Journal timestamp pattern, fall back to mtime.
    The most recently modified file wins.
    """
    old = _touch(tmp_path / "Journal.bad-name.01.log")
    new = _touch(tmp_path / "Journal.also-bad.02.log")

    # Make new have a clearly newer mtime
    import os

    os.utime(old, (1000000, 1000000))
    os.utime(new, (9999999, 9999999))

    watcher = _make_watcher(tmp_path)
    selected = watcher._find_current_journal()

    assert selected is not None
    assert selected.name == new.name


@pytest.mark.asyncio
async def test_2026_04_29_beats_older_journals(tmp_path: Path) -> None:
    """
    Regression test for the live telemetry failure on 2026-04-29.

    Three actual filenames from the user's journal directory:
      - Journal.2026-04-16T010942.01.log  (oldest)
      - Journal.2026-04-28T133233.01.log  (wrong selection during the failed test)
      - Journal.2026-04-29T144219.01.log  (correct — the active session)

    Must select Journal.2026-04-29T144219.01.log regardless of mtime ordering.
    """
    import os

    _touch(tmp_path / "Journal.2026-04-16T010942.01.log")
    wrong = _touch(tmp_path / "Journal.2026-04-28T133233.01.log")
    correct = _touch(tmp_path / "Journal.2026-04-29T144219.01.log")

    # Give the two older files much newer mtimes to simulate the failure condition
    future = time.time() + 7200
    os.utime(wrong, (future, future))
    os.utime(tmp_path / "Journal.2026-04-16T010942.01.log", (future + 1, future + 1))

    watcher = _make_watcher(tmp_path)
    selected = watcher._find_current_journal()

    assert selected is not None, "Expected a journal to be selected"
    assert selected.name == correct.name, (
        f"Expected Journal.2026-04-29T144219.01.log but got {selected.name}"
    )


def test_colon_variant_filename_parsed_unit() -> None:
    """
    _parse_journal_timestamp must handle Journal.YYYY-MM-DDTHH:MM:SS.NN.log
    (colon-separator variant). Windows forbids colons in filenames so we cannot
    create such a file in tmp_path; test the parser directly instead.
    """
    watcher = JournalWatcher(dispatch_fn=_noop)
    dt = watcher._parse_journal_timestamp("Journal.2026-04-29T14:42:19.01.log")
    assert dt is not None
    assert dt.year == 2026
    assert dt.month == 4
    assert dt.day == 29
    assert dt.hour == 14
    assert dt.minute == 42
    assert dt.second == 19
