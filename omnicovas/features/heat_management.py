"""
omnicovas.features.heat_management

Heat Management — Feature 10 (Pillar 1, Tier 2 — Rule-Based).

Handler: Status (dispatcher event from Status.json poll)
Publishes: HEAT_WARNING — on threshold crossing (0.80) with KB-grounded suggestion text
Tier 2: KB rules evaluated against heat level + trend.
Zero LLM calls. NullProvider-safe.

Rolling window: deque of last 10 heat readings for trend calculation.

Law 1: suggestion text in payload only; ConfirmationGate is Phase 3 UI concern
Law 5: broadcast on threshold crossing only — not every Status tick
Law 7: heat_level written with TelemetrySource.STATUS_JSON

Ref: Phase 2 Development Guide Week 9, Part E
Ref: Master Blueprint v4.2 — Pillar 1, Feature 10
"""

from __future__ import annotations

import logging
from collections import deque
from typing import Any

from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
from omnicovas.core.event_types import HEAT_WARNING
from omnicovas.core.state_manager import StateManager, TelemetrySource

logger = logging.getLogger(__name__)

# Threshold constants (KB-grounded)
_HEAT_WARNING_FRACTION: float = 0.80  # KB: combat_mechanics::heat_warning_threshold
_HEAT_CRITICAL_FRACTION: float = 0.95  # KB: combat_mechanics::heat_critical_threshold
_HEAT_DAMAGE_FRACTION: float = 1.20  # KB: combat_mechanics::heat_damage_threshold

# Rule string constants (KB-grounded)
# KB refs: heat_rule_high_heat_rising, heat_rule_critical,
#          heat_rule_steady_high, heat_rule_falling
_RULE_HIGH_RISING = "Reduce throttle and move away from heat sources"
_RULE_CRITICAL = "Critical heat — deploy heat sink or take evasive action immediately"
_RULE_STEADY_HIGH = "Sustained high heat — check modules for heat generation"
_RULE_FALLING = "Heat normalizing — thermal management effective"


def _compute_trend(buf: deque[float]) -> str:
    """Compute trend from rolling window of heat readings.

    Args:
        buf: deque of last up to 10 heat readings

    Returns:
        "rising", "falling", or "steady"
    """
    if len(buf) < 6:
        return "steady"

    first_avg = sum(list(buf)[:3]) / 3.0
    last_avg = sum(list(buf)[-3:]) / 3.0

    if last_avg - first_avg >= 0.05:
        return "rising"
    if first_avg - last_avg >= 0.05:
        return "falling"
    return "steady"


def _select_rule(heat: float, trend: str) -> str:
    """Select suggestion text based on heat level and trend.

    Args:
        heat: current heat level (0.0-1.0+)
        trend: "rising", "falling", or "steady"

    Returns:
        Suggestion string from KB rules
    """
    if heat >= _HEAT_CRITICAL_FRACTION:
        return _RULE_CRITICAL
    if trend == "rising":
        return _RULE_HIGH_RISING
    if trend == "falling":
        return _RULE_FALLING
    return _RULE_STEADY_HIGH


async def handle_status_heat(
    event: dict[str, Any],
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    heat_buffer: deque[float],
    prev_holder: dict[str, float | None],
) -> None:
    """Handle Status heat event — publish HEAT_WARNING on threshold crossing.

    Journal fields:
        Heat    -- 0.0-1.0+ float from Status.json

    Behavior:
        Only broadcasts HEAT_WARNING when heat crosses upward through
        _HEAT_WARNING_FRACTION (0.80). Suggestion text includes current
        heat level, trend, and KB-grounded rule.

    Args:
        event: Status event from Status.json poll
        state: The shared StateManager instance
        broadcaster: The shared ShipStateBroadcaster instance
        heat_buffer: deque of last 10 heat readings for trend calculation
        prev_holder: dict with "value" key holding previous heat or None
    """
    ts = event.get("timestamp")
    heat_raw = event.get("Heat")

    if heat_raw is None:
        return

    new_heat = float(heat_raw)
    heat_buffer.append(new_heat)

    state.update_field("heat_level", new_heat, TelemetrySource.STATUS_JSON, ts)

    trend = _compute_trend(heat_buffer)

    prev = prev_holder["value"]
    prev_holder["value"] = new_heat

    # Broadcast on upward crossing of warning threshold
    prev_below = prev is None or prev < _HEAT_WARNING_FRACTION

    if prev_below and new_heat >= _HEAT_WARNING_FRACTION:
        suggestion = _select_rule(new_heat, trend)
        threshold = (
            _HEAT_CRITICAL_FRACTION
            if new_heat >= _HEAT_CRITICAL_FRACTION
            else _HEAT_WARNING_FRACTION
        )
        logger.warning(
            "HEAT_WARNING: heat=%.2f trend=%s suggestion=%r",
            new_heat,
            trend,
            suggestion,
        )
        await broadcaster.publish(
            HEAT_WARNING,
            ShipStateEvent.now(
                HEAT_WARNING,
                {
                    "heat": new_heat,
                    "trend": trend,
                    "suggestion": suggestion,
                    "threshold": threshold,
                },
                source="status_json",
            ),
        )


def register(
    dispatcher_register: Any,
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
) -> None:
    """Register Heat Management handler with the EventDispatcher.

    Args:
        dispatcher_register: EventDispatcher.register method
        state: The shared StateManager instance (unused but kept for
            signature consistency)
        broadcaster: The shared ShipStateBroadcaster instance
    """
    heat_buffer: deque[float] = deque(maxlen=10)
    prev_holder: dict[str, float | None] = {"value": None}

    async def _status_heat(event: dict[str, Any]) -> None:
        await handle_status_heat(event, state, broadcaster, heat_buffer, prev_holder)

    dispatcher_register("Status", _status_heat)

    logger.info("Heat Management handler registered (Status)")
