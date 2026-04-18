"""
tests.test_dispatcher

Tests for the EventDispatcher.

Related to: Law 7 (Telemetry Rigidity) — every event must route correctly
Related to: Law 6 (Performance Priority) — handler exceptions never crash loop
Related to: Phase 1 Development Guide Week 2, Part B

Tests:
    1. Known event types route to correct handler
    2. Unknown event types are ignored without crashing
    3. Handler exceptions are caught (dispatcher stays alive)
    4. Malformed JSON is skipped without crashing
    5. Multiple handlers per event type all get called
"""

from __future__ import annotations

from typing import Any

import pytest

from omnicovas.core.dispatcher import EventDispatcher


@pytest.mark.asyncio
async def test_known_event_routes_to_handler() -> None:
    """
    Verify a known event type routes to the correct registered handler.
    """
    received: list[dict[str, Any]] = []

    async def capture_handler(event: dict[str, Any]) -> None:
        received.append(event)

    dispatcher = EventDispatcher()
    dispatcher.register("FSDJump", capture_handler)

    line = '{"timestamp":"2026-01-01","event":"FSDJump","StarSystem":"Sol"}'
    await dispatcher.dispatch(line)

    assert len(received) == 1
    assert received[0]["event"] == "FSDJump"
    assert received[0]["StarSystem"] == "Sol"


@pytest.mark.asyncio
async def test_unknown_event_ignored_without_crash() -> None:
    """
    Verify unknown event types are silently ignored.
    Dispatcher must not crash on unregistered event types.
    """
    dispatcher = EventDispatcher()

    await dispatcher.dispatch('{"timestamp":"2026-01-01","event":"UnknownEvent"}')

    assert dispatcher.events_processed == 1


@pytest.mark.asyncio
async def test_handler_exception_does_not_crash_dispatcher() -> None:
    """
    Verify handler exceptions are caught and logged.
    The dispatcher must survive a broken handler.

    Related to: Law 6 (Performance Priority) — zero cascade failures
    """

    async def broken_handler(event: dict[str, Any]) -> None:
        raise RuntimeError("Simulated handler failure")

    async def good_handler(event: dict[str, Any]) -> None:
        pass

    dispatcher = EventDispatcher()
    dispatcher.register("FSDJump", broken_handler)
    dispatcher.register("FSDJump", good_handler)

    await dispatcher.dispatch('{"timestamp":"2026-01-01","event":"FSDJump"}')

    assert dispatcher.events_processed == 1


@pytest.mark.asyncio
async def test_malformed_json_skipped_without_crash() -> None:
    """
    Verify malformed JSON lines are skipped gracefully.
    Dispatcher must not crash on bad input.
    """
    dispatcher = EventDispatcher()

    await dispatcher.dispatch("this is not json {{{")
    await dispatcher.dispatch("")
    await dispatcher.dispatch("{incomplete")

    assert dispatcher.events_processed == 0


@pytest.mark.asyncio
async def test_multiple_handlers_all_called() -> None:
    """
    Verify multiple handlers registered for the same event type
    are all called (publish/subscribe pattern).
    """
    call_log: list[str] = []

    async def handler_a(event: dict[str, Any]) -> None:
        call_log.append("A")

    async def handler_b(event: dict[str, Any]) -> None:
        call_log.append("B")

    async def handler_c(event: dict[str, Any]) -> None:
        call_log.append("C")

    dispatcher = EventDispatcher()
    dispatcher.register("Docked", handler_a)
    dispatcher.register("Docked", handler_b)
    dispatcher.register("Docked", handler_c)

    line = '{"timestamp":"2026-01-01","event":"Docked","StationName":"Jameson"}'
    await dispatcher.dispatch(line)

    assert call_log == ["A", "B", "C"]
    assert dispatcher.events_processed == 1


@pytest.mark.asyncio
async def test_events_processed_counter() -> None:
    """
    Verify events_processed counts only successfully parsed events.
    """
    dispatcher = EventDispatcher()

    await dispatcher.dispatch('{"event":"FSDJump"}')
    await dispatcher.dispatch('{"event":"Docked"}')
    await dispatcher.dispatch("bad json")

    assert dispatcher.events_processed == 2
