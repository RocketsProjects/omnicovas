"""
tests.test_latency_budgets

Tests for the Latency Budget Framework -- Week 7 Part F.

These tests verify the framework mechanics: budget lookup, CI detection,
warning on breach, and no-op on unknown event types. They do NOT enforce
dispatch-time hard-fails yet -- that flip happens in Week 9 when handlers
are fully implemented and tuned.

The four required tests from the Phase 2 Development Guide:
    1. Fast handler under budget produces no warning
    2. Slow handler produces a warning with correct fields
    3. Unknown event type passes through without error
    4. CI mode doubles the budget

Related to: Phase 2 Development Guide Week 7, Part F
Related to: Master Blueprint v4.1 Section 14 (Performance Commitments)
Related to: Law 6 (Performance Priority) -- zero lag, function first
"""

from __future__ import annotations

import asyncio
import logging
from unittest.mock import patch

import pytest

from omnicovas.core.latency import (
    BUDGETS,
    BudgetedDispatcher,
    effective_budget_ms,
    in_ci_environment,
    measure,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _FakeDispatcher:
    """Minimal dispatcher stub for latency tests."""

    def __init__(self, sleep_ms: float = 0.0) -> None:
        self._sleep_ms = sleep_ms
        self.events_processed = 0

    async def dispatch(self, raw_line: str) -> None:
        if self._sleep_ms > 0:
            await asyncio.sleep(self._sleep_ms / 1000.0)
        self.events_processed += 1


def _hull_damage_line() -> str:
    return '{"timestamp":"2026-04-19T12:00:00Z","event":"HullDamage","Health":0.8}'


def _unknown_line() -> str:
    return '{"timestamp":"2026-04-19T12:00:00Z","event":"SupercruiseEntry"}'


# ---------------------------------------------------------------------------
# Test 1: Fast handler under budget -- no warning
# ---------------------------------------------------------------------------


async def test_fast_handler_produces_no_warning(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """A handler that completes well under budget must not log a warning.

    Law 6: warnings are a signal of real performance problems, not noise.
    """
    dispatcher = _FakeDispatcher(sleep_ms=0.0)
    budgeted = BudgetedDispatcher(dispatcher)

    with caplog.at_level(logging.WARNING, logger="omnicovas.core.latency"):
        await budgeted.dispatch(_hull_damage_line())

    breach_warnings = [
        r for r in caplog.records if "latency_budget_exceeded" in r.getMessage()
    ]
    assert len(breach_warnings) == 0


# ---------------------------------------------------------------------------
# Test 2: Slow handler produces a warning with correct fields
# ---------------------------------------------------------------------------


async def test_slow_handler_produces_warning(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """A handler that exceeds its budget must log a warning.

    HullDamage budget is 100ms locally. We sleep 150ms to force a breach.
    """
    dispatcher = _FakeDispatcher(sleep_ms=150.0)
    budgeted = BudgetedDispatcher(dispatcher)

    with caplog.at_level(logging.WARNING, logger="omnicovas.core.latency"):
        with patch.dict("os.environ", {"CI": ""}, clear=False):
            await budgeted.dispatch(_hull_damage_line())

    breach_warnings = [
        r for r in caplog.records if "latency_budget_exceeded" in r.getMessage()
    ]
    assert len(breach_warnings) == 1


# ---------------------------------------------------------------------------
# Test 3: Unknown event type passes through without error
# ---------------------------------------------------------------------------


async def test_unknown_event_type_no_error(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """An event type not in BUDGETS must dispatch without crashing or warning.

    Future event types should not break the framework before they are budgeted.
    """
    assert "SupercruiseEntry" not in BUDGETS

    dispatcher = _FakeDispatcher(sleep_ms=0.0)
    budgeted = BudgetedDispatcher(dispatcher)

    # Must not raise
    await budgeted.dispatch(_unknown_line())

    breach_warnings = [
        r for r in caplog.records if "latency_budget_exceeded" in r.getMessage()
    ]
    assert len(breach_warnings) == 0


# ---------------------------------------------------------------------------
# Test 4: CI mode doubles the budget
# ---------------------------------------------------------------------------


def test_ci_mode_doubles_budget() -> None:
    """effective_budget_ms() must return 2x the local budget in CI."""
    local_budget = BUDGETS["HullDamage"].budget_ms  # 100ms

    with patch.dict("os.environ", {"CI": "true"}, clear=False):
        ci_budget = effective_budget_ms("HullDamage")

    assert ci_budget == local_budget * 2


def test_local_mode_uses_budget_as_is() -> None:
    """effective_budget_ms() must return the exact budget locally."""
    local_budget = BUDGETS["HullDamage"].budget_ms  # 100ms

    with patch.dict("os.environ", {}, clear=True):
        local_effective = effective_budget_ms("HullDamage")

    assert local_effective == local_budget


def test_unknown_event_returns_none_budget() -> None:
    """effective_budget_ms() must return None for unregistered event types."""
    result = effective_budget_ms("SupercruiseEntry")
    assert result is None


# ---------------------------------------------------------------------------
# CI detection
# ---------------------------------------------------------------------------


def test_in_ci_environment_true_when_ci_set() -> None:
    """in_ci_environment() must return True when CI env var is set."""
    with patch.dict("os.environ", {"CI": "true"}, clear=False):
        assert in_ci_environment() is True


def test_in_ci_environment_false_when_ci_not_set() -> None:
    """in_ci_environment() must return False when CI is absent."""
    env = {k: v for k, v in __import__("os").environ.items() if k != "CI"}
    with patch.dict("os.environ", env, clear=True):
        assert in_ci_environment() is False


# ---------------------------------------------------------------------------
# measure() helper
# ---------------------------------------------------------------------------


async def test_measure_returns_elapsed_ms() -> None:
    """measure() must return a positive elapsed time."""

    async def noop() -> None:
        pass

    elapsed = await measure("HullDamage", noop())
    assert elapsed >= 0.0


async def test_measure_slow_coro_returns_large_elapsed() -> None:
    """measure() elapsed must reflect actual sleep time."""

    async def slow() -> None:
        await asyncio.sleep(0.05)

    elapsed = await measure("FSDJump", slow())
    assert elapsed >= 40.0  # generous lower bound


# ---------------------------------------------------------------------------
# BUDGETS completeness
# ---------------------------------------------------------------------------


def test_all_week7_event_types_are_budgeted() -> None:
    """Every event type introduced in Week 7 must have a budget entry."""
    week7_events = {
        "HullDamage",
        "ShieldsDown",
        "FSDJump",
        "Docked",
        "Undocked",
        "Loadout",
        "Status",
    }
    missing = week7_events - set(BUDGETS.keys())
    assert not missing, f"Missing budget entries: {missing}"


def test_all_week9_event_types_are_budgeted() -> None:
    """Every new journal event type introduced in Week 9 must have a budget entry."""
    week9_events = {
        "Cargo",
        "CommitCrime",
        "Bounty",
        "ShipDestroyed",
        "Died",
        "ShieldsUp",
    }
    missing = week9_events - set(BUDGETS.keys())
    assert not missing, f"Missing budget entries for Week 9 events: {missing}"
