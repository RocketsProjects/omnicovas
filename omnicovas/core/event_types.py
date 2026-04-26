"""Pillar 1 event-type string constants — single source of truth.

Every ``broadcaster.subscribe(...)`` and ``broadcaster.publish(...)`` call
references a constant defined here. Importing a bad constant name raises
``ImportError`` at module-load time; using a magic string silently
registers a subscription that will never fire. The whole point of this
file is to make that second failure mode impossible.

New event types added in later Phase 2 weeks extend this module only —
they do not live in feature files. This keeps the Seven-Layer Debugging
Vocabulary layer boundary (layer 5 — broadcaster) sharp.

References:
    * Master Blueprint v4.1, Section 11 (Fault Tolerance — subscriber isolation).
    * Phase 2 Development Guide, Week 7 Part A, task 1.
    * Phase 2 Development Guide, Pillar 1 Event Type Reference (appendix).
    * CLAUDE.md Pattern 1 (Event Broadcasting).
"""

from __future__ import annotations

from typing import Final

# --- Core lifecycle ---------------------------------------------------------
# Published whenever any field of the ship's identity/state block changes
# enough that downstream subscribers may want a coalesced "something moved"
# signal. Fine-grained events below are the canonical path; SHIP_STATE_CHANGED
# is the catch-all for UI refreshes and Activity-Log summaries.
SHIP_STATE_CHANGED: Final[str] = "SHIP_STATE_CHANGED"
LOADOUT_CHANGED: Final[str] = "LOADOUT_CHANGED"

# --- Hull & shield (Week 9 — Hull & Integrity Triggers) ---------------------
# HULL_DAMAGE fires on every HullDamage journal event (combat subscribers).
# HULL_CRITICAL_* fire exactly once per downward threshold crossing.
HULL_DAMAGE: Final[str] = "HULL_DAMAGE"
HULL_CRITICAL_25: Final[str] = "HULL_CRITICAL_25"
HULL_CRITICAL_10: Final[str] = "HULL_CRITICAL_10"
SHIELDS_DOWN: Final[str] = "SHIELDS_DOWN"
SHIELDS_UP: Final[str] = "SHIELDS_UP"

# --- Fuel (Week 7 Parts C/D — Fuel & Jump Range) ----------------------------
FUEL_LOW: Final[str] = "FUEL_LOW"
FUEL_CRITICAL: Final[str] = "FUEL_CRITICAL"
RESERVOIR_REPLENISHED: Final[str] = "RESERVOIR_REPLENISHED"

# --- Navigation & location (Week 9 Part C — Extended Event Broadcaster) -----
FSD_JUMP: Final[str] = "FSD_JUMP"
DOCKED: Final[str] = "DOCKED"
UNDOCKED: Final[str] = "UNDOCKED"

# --- Commander status (Week 9 Part C) ---------------------------------------
# WANTED is per-system and clears on FSD jump to a different system.
WANTED: Final[str] = "WANTED"
DESTROYED: Final[str] = "DESTROYED"

# --- Power distribution (Week 9 Part D) -------------------------------------
PIPS_CHANGED: Final[str] = "PIPS_CHANGED"

# --- Heat management (Week 9 Part E — Tier 2) -------------------------------
HEAT_WARNING: Final[str] = "HEAT_WARNING"

# --- Cargo (Week 8 — Cargo Monitoring) --------------------------------------
CARGO_CHANGED: Final[str] = "CARGO_CHANGED"

# --- Modules (Week 8 Module Health + Week 9 Critical Event Broadcaster) -----
# MODULE_DAMAGED fires when a module's health crosses below 80%.
# MODULE_CRITICAL fires when a module's health crosses below 20%.
MODULE_DAMAGED: Final[str] = "MODULE_DAMAGED"
MODULE_CRITICAL: Final[str] = "MODULE_CRITICAL"


# Audit aid: every constant exported by this module. Used by the Week 9
# Critical Event Broadcaster audit test to guarantee no event-type
# constant is referenced before it is declared here.
ALL_EVENT_TYPES: Final[frozenset[str]] = frozenset(
    {
        SHIP_STATE_CHANGED,
        LOADOUT_CHANGED,
        HULL_DAMAGE,
        HULL_CRITICAL_25,
        HULL_CRITICAL_10,
        SHIELDS_DOWN,
        SHIELDS_UP,
        FUEL_LOW,
        FUEL_CRITICAL,
        RESERVOIR_REPLENISHED,
        FSD_JUMP,
        DOCKED,
        UNDOCKED,
        WANTED,
        DESTROYED,
        PIPS_CHANGED,
        HEAT_WARNING,
        CARGO_CHANGED,
        MODULE_DAMAGED,
        MODULE_CRITICAL,
    }
)

# The six criticals audited by the Week 9 Critical Event Broadcaster test.
# Matches Phase 2 Development Guide, Week 9 Part B, task 1 exactly.
CRITICAL_EVENT_TYPES: Final[frozenset[str]] = frozenset(
    {
        HULL_CRITICAL_25,
        HULL_CRITICAL_10,
        SHIELDS_DOWN,
        FUEL_LOW,
        FUEL_CRITICAL,
        MODULE_CRITICAL,
    }
)
