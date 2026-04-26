Phase 2, Week 8 Part A prerequisite — close the fuel-capacity split that was started in a prior session.
A previous refactor split SessionState.fuel_capacity into fuel_capacity_main and fuel_capacity_reserve. SessionState and features/ship_state.py.handle_loadout were updated. The remaining work is mechanical fixes to indentation, a stale docstring, and stale test references. No architectural decisions; do not add features or change behavior.
Architectural note (do not change): FSDJump is registered by both core/handlers.py.handle_fsd_jump (location concern) and features/fuel.py.handle_fsdjump (fuel concern). The dispatcher supports multiple handlers per event type. This is intentional separation of concerns, verified by tests/test_dispatcher.py test_multiple_handlers_all_called.
Make exactly these edits, in this order:

omnicovas/features/fuel.py — fix the IndentationError in handle_refuel_all (function body indented 8 spaces instead of 4) and the matching inconsistency in handle_refuel_partial. Function bodies are 4 spaces; lines inside the if amount is not None: blocks are 8 spaces. Pure whitespace; do not change logic, control flow, arguments, or any string.
omnicovas/features/fuel.py — in _check_thresholds(), the payload dict has the key "fuel_capacity". Rename that key to "fuel_capacity_main". This is a broadcaster payload label, not a state field write.
omnicovas/features/fuel.py — in register(), append a Note section to the docstring after the existing Args block, before the inner async def lines:
Note:
    FSDJump is also registered by core/handlers.py.handle_fsd_jump
    (location concern: current_system, is_in_supercruise). The
    handler here updates fuel_main and fuel_reservoir from the
    FSDJump payload. Both run; the dispatcher supports multiple
    handlers per event type. Intentional separation of concerns,
    not a bug.

omnicovas/features/ship_state.py — in handle_loadout's docstring, replace the line:
FuelCapacity  -> fuel_capacity (FuelCapacity.Main, tons)
with these two lines, preserving column alignment:
FuelCapacity.Main    -> fuel_capacity_main (tons)
FuelCapacity.Reserve -> fuel_capacity_reserve (tons)

tests/test_live_ship_state.py — rename test_loadout_sets_fuel_capacity to test_loadout_sets_fuel_capacities and replace its body with:
async def test_loadout_sets_fuel_capacities(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """Loadout must extract both Main and Reserve fuel capacity."""
    await handle_loadout(make_loadout(fuel_main=32.0), state, broadcaster)
    assert state.snapshot.fuel_capacity_main == pytest.approx(32.0)
    assert state.snapshot.fuel_capacity_reserve == pytest.approx(0.5)
Do not change make_loadout. The 0.5 value comes from its existing FuelCapacity.Reserve default.
tests/test_fuel.py — replace the set_fuel helper with:
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
Then update every set_fuel call site in this file: change keyword capacity= to capacity_main=. Numeric values stay identical.
tests/test_fuel.py — in test_no_threshold_on_first_fuel_reading, change:
state.update_field("fuel_capacity", 32.0, TelemetrySource.JOURNAL)
to:
state.update_field("fuel_capacity_main", 32.0, TelemetrySource.JOURNAL)

test_no_threshold_without_capacity sets fuel_main only and does not reference fuel_capacity by name. Verify, do not edit.

After the edits run:
pytest -q
mypy --strict omnicovas/
ruff check omnicovas/
Acceptance: pytest collects cleanly, all 84 Phase 1 tests pass, all test_fuel.py and test_live_ship_state.py tests pass. mypy strict green. ruff clean.
If a test fails, that is a real bug exposed by collection finally working. Stop and report it. Do not invent assertions or change handler logic to make tests pass.
Do not modify state_manager.py, handlers.py, event_types.py, broadcaster.py, or main.py. Do not add new tests. Do not change make_loadout, make_scoop, make_refuel_all, or make_refuel_partial.
