# Playbook: PB-02 -- Fuel Test Cleanup + Fuel Split Stragglers

Phase: 2, Week 8 Part A prerequisite (final closure)
Authority: CLAUDE.MD Section XV; Soldier.md Section 0
Estimated turns: 1
Predecessor: 662fc4a (Phase 2 Week 7 close-out)

---

## Context

PB-01 partially landed in commit 662fc4a. Five tests still fail because
test fixtures reference the deleted `fuel_capacity` field. Production code
also has two stragglers: a stale broadcast payload key and a stale
docstring. The Note section in fuel.py.register() about dual FSDJump
registration is missing and must be restored.

This Playbook closes all of it. No architectural changes. No new logic.
No new tests. Test-fixture renames, one-character payload key rename,
two-line docstring fix, multi-line docstring restoration.

---

## Files to Tag in Continue

@Soldier.md
@omnicovas/features/fuel.py
@omnicovas/features/ship_state.py
@tests/test_fuel.py
@tests/test_live_ship_state.py

---

## Soldier Prompt

Phase 2 close-out. Make exactly these 8 edits. Do not add features.
Do not add tests. Do not modify behavior. Do not touch any file not
listed below.

EDIT 1 -- omnicovas/features/fuel.py

In _check_thresholds(), the payload dict currently has the key
"fuel_capacity". Rename that single key to "fuel_capacity_main".
This is a broadcaster payload label. Find:

    "fuel_capacity": capacity,

Replace with:

    "fuel_capacity_main": capacity,

EDIT 2 -- omnicovas/features/fuel.py

In register(), restore the Note section to the docstring. Currently
the docstring is:

    """Register all Fuel & Jump Range handlers with the EventDispatcher.

    Args:
        dispatcher_register: EventDispatcher.register method
        state: The shared StateManager instance
        broadcaster: The shared ShipStateBroadcaster instance
    """

Replace with:

    """Register all Fuel & Jump Range handlers with the EventDispatcher.

    Args:
        dispatcher_register: EventDispatcher.register method
        state: The shared StateManager instance
        broadcaster: The shared ShipStateBroadcaster instance

    Note:
        FSDJump is also registered by core/handlers.py.handle_fsd_jump
        (location concern: current_system, is_in_supercruise). The
        handler here updates fuel_main and fuel_reservoir from the
        FSDJump payload. Both run; the dispatcher supports multiple
        handlers per event type. Intentional separation of concerns,
        not a bug.
    """

EDIT 3 -- omnicovas/features/ship_state.py

In handle_loadout's docstring, replace the line:

        FuelCapacity  -> fuel_capacity (FuelCapacity.Main, tons)

with these two lines, preserving column alignment with surrounding
docstring lines:

        FuelCapacity.Main    -> fuel_capacity_main (tons)
        FuelCapacity.Reserve -> fuel_capacity_reserve (tons)

EDIT 4 -- tests/test_fuel.py

Replace the set_fuel helper function. Find:

    def set_fuel(
        state: StateManager,
        main: float,
        capacity: float,
    ) -> None:
        """Helper: pre-populate fuel state so threshold tests have context."""
        state.update_field("fuel_main", main, TelemetrySource.STATUS_JSON)
        state.update_field("fuel_capacity", capacity, TelemetrySource.JOURNAL)

Replace with:

    def set_fuel(
        state: StateManager,
        main: float,
        capacity_main: float,
    ) -> None:
        """Helper: pre-populate fuel state so threshold tests have context."""
        state.update_field("fuel_main", main, TelemetrySource.STATUS_JSON)
        state.update_field(
            "fuel_capacity_main", capacity_main, TelemetrySource.JOURNAL
        )

EDIT 5 -- tests/test_fuel.py

Update every call site of set_fuel in this file. Each call currently
uses the keyword argument `capacity=`. Change every occurrence to
`capacity_main=`. The numeric values stay identical. There are
multiple call sites. Update all of them.

EDIT 6 -- tests/test_fuel.py

In the function test_no_threshold_on_first_fuel_reading, find:

    state.update_field("fuel_capacity", 32.0, TelemetrySource.JOURNAL)

Replace with:

    state.update_field("fuel_capacity_main", 32.0, TelemetrySource.JOURNAL)

EDIT 7 -- tests/test_live_ship_state.py

Rename the function test_loadout_sets_fuel_capacity to
test_loadout_sets_fuel_capacities and replace its body. Find the
entire current function:

    async def test_loadout_sets_fuel_capacity(
        state: StateManager, broadcaster: ShipStateBroadcaster
    ) -> None:
        """Loadout must extract fuel capacity from FuelCapacity.Main."""
        await handle_loadout(make_loadout(fuel_main=32.0), state, broadcaster)
        assert state.snapshot.fuel_capacity == pytest.approx(32.0)

Replace with:

    async def test_loadout_sets_fuel_capacities(
        state: StateManager, broadcaster: ShipStateBroadcaster
    ) -> None:
        """Loadout must extract both Main and Reserve fuel capacity."""
        await handle_loadout(make_loadout(fuel_main=32.0), state, broadcaster)
        assert state.snapshot.fuel_capacity_main == pytest.approx(32.0)
        assert state.snapshot.fuel_capacity_reserve == pytest.approx(0.5)

EDIT 8 -- verification

Do not edit anything else. After making edits 1-7, run:

    pytest -q
    mypy --strict omnicovas/
    ruff check omnicovas/

Acceptance:

  - pytest reports 157 passed, 0 failed (the 5 tests that previously
    failed are the ones fixed by edits 4, 5, 6, 7).
  - mypy strict: zero errors
  - ruff: zero violations

If any test fails after these edits, that is a real bug. Stop and
report it via ESCALATE per Soldier.md Rule 4. Do not invent
assertions or change handler logic to make tests pass.

Do not modify omnicovas/core/state_manager.py. Do not modify
omnicovas/core/handlers.py. Do not modify omnicovas/core/event_types.py.
Do not modify omnicovas/core/broadcaster.py. Do not modify any other
file in the repository.

---

## Verification

Run from project root:

    pytest -q
    mypy --strict omnicovas/
    ruff check omnicovas/

Expected: 157 passed, 0 failed. mypy clean. ruff clean.

---

## Out of Scope

Do not address in this Playbook:

  - Doc drift items in CLAUDE.MD (hull scale, fuel_current vs fuel_main)
  - Doc drift in Soldier.md Section 13 event names
  - Week 8 Part A proper (parse_modules, ModuleInfo, fixtures)
  - The state.py vs state_manager.py path question
  - The features/loadout.py vs ship_state.py path question

These are separate Playbooks.

---

## Commit Message (Commander use after green test run)

    fix(phase2): close fuel-capacity split — fix 5 failing tests, restore FSDJump Note, update payload key

---

END OF PB-02
