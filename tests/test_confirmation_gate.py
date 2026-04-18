"""
tests.test_confirmation_gate

Tests for the Confirmation Gate — Law 1 enforcement.

Related to: Law 1 (Confirmation Gate) — THE most important law
Related to: Law 8 (Sovereignty & Transparency) — audit log is permanent
Related to: Phase 1 Development Guide Week 4, Part C

Tests:
    1. Phase 1 auto-approve returns True
    2. auto_approve=False denies every request (simulates "no UI yet")
    3. Every request is recorded in the audit log
    4. Audit log entries are immutable from the outside (ConfirmationRecord frozen)
    5. total_requests counter is accurate
    6. ActionType enum rejects arbitrary strings (must use defined members)
    7. details dict is copied into the audit record (caller mutation can't corrupt)
    8. Decision is stored correctly in the record
    9. Multiple sequential requests each produce a record
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from omnicovas.core.confirmation_gate import (
    ActionType,
    ConfirmationDecision,
    ConfirmationGate,
    ConfirmationRecord,
)


@pytest.mark.asyncio
async def test_auto_approve_returns_true() -> None:
    """Phase 1 default: auto_approve=True causes APPROVED decisions."""
    gate = ConfirmationGate(auto_approve=True)

    approved = await gate.require_confirmation(
        action_type=ActionType.PLOT_ROUTE,
        summary="Plot route to Sol",
    )

    assert approved is True


@pytest.mark.asyncio
async def test_no_auto_approve_denies_request() -> None:
    """
    Law 1: without auto_approve (simulating "no UI yet"), the gate
    denies every request. Proves the pipeline cannot be bypassed.
    """
    gate = ConfirmationGate(auto_approve=False)

    approved = await gate.require_confirmation(
        action_type=ActionType.COMBAT_ALERT,
        summary="Hostile inbound",
    )

    assert approved is False


@pytest.mark.asyncio
async def test_every_request_recorded_in_audit_log() -> None:
    """Law 8: every confirmation event is permanently audit-logged."""
    gate = ConfirmationGate(auto_approve=True)

    await gate.require_confirmation(
        action_type=ActionType.PLOT_ROUTE,
        summary="Route 1",
    )
    await gate.require_confirmation(
        action_type=ActionType.COMBAT_ALERT,
        summary="Alert 1",
    )

    log = gate.audit_log
    assert len(log) == 2
    assert log[0].action_type == ActionType.PLOT_ROUTE
    assert log[1].action_type == ActionType.COMBAT_ALERT


@pytest.mark.asyncio
async def test_audit_record_is_immutable() -> None:
    """
    ConfirmationRecord is frozen — it cannot be mutated after creation.
    This protects the audit trail from tampering.
    """
    gate = ConfirmationGate(auto_approve=True)
    await gate.require_confirmation(
        action_type=ActionType.PLOT_ROUTE,
        summary="Test",
    )

    record = gate.audit_log[0]

    with pytest.raises(FrozenInstanceError):
        record.summary = "Tampered"  # type: ignore[misc]


@pytest.mark.asyncio
async def test_audit_log_returns_copy() -> None:
    """
    audit_log property returns a copy — mutating the returned list
    must not affect the gate's internal state.
    """
    gate = ConfirmationGate(auto_approve=True)
    await gate.require_confirmation(
        action_type=ActionType.PLOT_ROUTE,
        summary="Test",
    )

    log_copy = gate.audit_log
    log_copy.clear()

    assert gate.total_requests == 1
    assert len(gate.audit_log) == 1


@pytest.mark.asyncio
async def test_total_requests_counter() -> None:
    """total_requests must match the number of confirmations requested."""
    gate = ConfirmationGate(auto_approve=True)

    assert gate.total_requests == 0

    for _ in range(5):
        await gate.require_confirmation(
            action_type=ActionType.INFORMATION_ONLY,
            summary="Test",
        )

    assert gate.total_requests == 5


def test_action_type_enum_rejects_arbitrary_strings() -> None:
    """
    ActionType is a closed enum — you cannot invent new action types at runtime.
    This forces adding new action types to be a deliberate code change.
    """
    with pytest.raises(ValueError):
        ActionType("some_undefined_action")


@pytest.mark.asyncio
async def test_details_dict_copied_into_record() -> None:
    """
    Mutating the caller's details dict after the fact must not corrupt
    the audit record. The gate must snapshot the details at call time.
    """
    gate = ConfirmationGate(auto_approve=True)
    details = {"destination": "Sol"}

    await gate.require_confirmation(
        action_type=ActionType.PLOT_ROUTE,
        summary="Test",
        details=details,
    )

    # Tamper with the original dict after the call
    details["destination"] = "Colonia"

    # The record should still show the original value
    assert gate.audit_log[0].details["destination"] == "Sol"


@pytest.mark.asyncio
async def test_decision_stored_correctly() -> None:
    """
    When auto_approve is True, the decision in the record is APPROVED.
    When auto_approve is False, it is REJECTED.
    """
    approving = ConfirmationGate(auto_approve=True)
    denying = ConfirmationGate(auto_approve=False)

    await approving.require_confirmation(
        action_type=ActionType.PLOT_ROUTE, summary="Yes"
    )
    await denying.require_confirmation(action_type=ActionType.PLOT_ROUTE, summary="No")

    assert approving.audit_log[0].decision == ConfirmationDecision.APPROVED
    assert denying.audit_log[0].decision == ConfirmationDecision.REJECTED


@pytest.mark.asyncio
async def test_each_request_produces_its_own_record() -> None:
    """Sequential calls each produce a distinct audit record in order."""
    gate = ConfirmationGate(auto_approve=True)

    actions = [
        (ActionType.PLOT_ROUTE, "A"),
        (ActionType.COMBAT_ALERT, "B"),
        (ActionType.SUGGEST_TRADE_ROUTE, "C"),
    ]

    for action_type, summary in actions:
        await gate.require_confirmation(action_type=action_type, summary=summary)

    log = gate.audit_log
    assert [r.summary for r in log] == ["A", "B", "C"]
    assert [r.action_type for r in log] == [a[0] for a in actions]


def test_confirmation_record_fields() -> None:
    """Smoke test: ConfirmationRecord has the expected fields."""
    record = ConfirmationRecord(
        action_type=ActionType.INFORMATION_ONLY,
        summary="test",
        details={},
        decision=ConfirmationDecision.APPROVED,
    )
    assert record.action_type == ActionType.INFORMATION_ONLY
    assert record.summary == "test"
    assert record.decision == ConfirmationDecision.APPROVED
    assert record.timestamp is not None
