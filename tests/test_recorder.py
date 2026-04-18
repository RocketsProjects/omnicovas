"""
tests.test_recorder

Tests for the EventRecorder database persistence layer.

Related to: Law 8 (Sovereignty & Transparency) — all events logged locally
Related to: Phase 1 Development Guide Week 3, Part B

Tests:
    1. start_session creates a session row
    2. record_event persists to the database
    3. end_session stamps end_time
    4. record_event without active session is dropped safely
    5. events_recorded counter is accurate
    6. Multiple events within a session share session_id
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from sqlalchemy import select

from omnicovas.db.engine import init_database, make_session_factory
from omnicovas.db.models import JournalEvent, Session
from omnicovas.db.recorder import EventRecorder


@pytest.fixture
async def recorder_and_factory():
    """
    Provide an EventRecorder bound to a temporary database.

    Uses a fresh tempfile per test for isolation.
    """
    tmpdir = tempfile.mkdtemp(prefix="omnicovas_test_")
    db_path = Path(tmpdir) / "test.db"
    engine = await init_database(db_path=db_path)
    factory = make_session_factory(engine)
    recorder = EventRecorder(factory)
    try:
        yield recorder, factory
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_start_session_creates_row(recorder_and_factory) -> None:
    """
    start_session must create a Session row and return its ID.
    """
    recorder, factory = recorder_and_factory

    session_id = await recorder.start_session(journal_filename="Journal.test.log")

    assert session_id >= 1
    async with factory() as db:
        result = await db.execute(select(Session).where(Session.id == session_id))
        session_row = result.scalar_one()
        assert session_row.journal_filename == "Journal.test.log"
        assert session_row.start_time is not None
        assert session_row.end_time is None


@pytest.mark.asyncio
async def test_record_event_persists(recorder_and_factory) -> None:
    """
    record_event must persist an event tied to the active session.
    """
    recorder, factory = recorder_and_factory
    await recorder.start_session(journal_filename="Journal.test.log")

    event = {
        "timestamp": "2026-04-18T12:00:00Z",
        "event": "FSDJump",
        "StarSystem": "Sol",
    }
    await recorder.record_event(event, '{"event":"FSDJump"}')

    async with factory() as db:
        result = await db.execute(select(JournalEvent))
        events = result.scalars().all()
        assert len(events) == 1
        assert events[0].event_type == "FSDJump"


@pytest.mark.asyncio
async def test_end_session_stamps_end_time(recorder_and_factory) -> None:
    """
    end_session must set end_time on the active Session row.
    """
    recorder, factory = recorder_and_factory
    session_id = await recorder.start_session(journal_filename="Journal.test.log")

    await recorder.end_session()

    async with factory() as db:
        result = await db.execute(select(Session).where(Session.id == session_id))
        session_row = result.scalar_one()
        assert session_row.end_time is not None


@pytest.mark.asyncio
async def test_record_event_without_session_drops_safely(recorder_and_factory) -> None:
    """
    If no session is active, record_event must not crash.
    """
    recorder, factory = recorder_and_factory

    event = {"event": "FSDJump"}
    await recorder.record_event(event, '{"event":"FSDJump"}')

    async with factory() as db:
        result = await db.execute(select(JournalEvent))
        events = result.scalars().all()
        assert len(events) == 0


@pytest.mark.asyncio
async def test_events_recorded_counter(recorder_and_factory) -> None:
    """
    events_recorded must match the number of persisted events.
    """
    recorder, factory = recorder_and_factory
    await recorder.start_session(journal_filename="Journal.test.log")

    for _ in range(5):
        await recorder.record_event(
            {"event": "FSDJump", "timestamp": "2026-04-18T12:00:00Z"},
            '{"event":"FSDJump"}',
        )

    assert recorder.events_recorded == 5


@pytest.mark.asyncio
async def test_multiple_events_share_session_id(recorder_and_factory) -> None:
    """
    All events recorded within one start/end must share the session_id.
    """
    recorder, factory = recorder_and_factory
    session_id = await recorder.start_session(journal_filename="Journal.test.log")

    for event_type in ["FSDJump", "Docked", "Undocked"]:
        await recorder.record_event(
            {"event": event_type, "timestamp": "2026-04-18T12:00:00Z"},
            f'{{"event":"{event_type}"}}',
        )

    async with factory() as db:
        result = await db.execute(select(JournalEvent))
        events = result.scalars().all()
        assert len(events) == 3
        assert all(e.session_id == session_id for e in events)
