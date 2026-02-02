# Simulation Structure Plan

The README personas describe commuter and tourist flows; this plan captures how the codebase will grow in small, teachable steps.

## Step 1 – Define Core Building Blocks

- Draft `stations.py`, `bikes.py`, and `personas.py` modules with dataclasses for stations, bike inventory snapshots, and rider demand profiles.
- Mirror those modules with pytest files under `tests/` to validate constructors and helper behaviors.
- Introduce clear module-level constants (e.g., default station capacity) with short comments that explain the choice.

## Step 2 – Persona Behaviors

- Flesh out commuter and tourist scheduling helpers that transform demand profiles into trip intents.
- Cover branching logic (morning/evening returns) with unit tests so personas remain predictable.

## Step 3 – Routing & Time Utilities

- Add `routes.py` for travel time estimates and basic path selection helpers.
- Keep functions small (e.g., `estimate_travel_minutes()`) and test them with deterministic fixtures.

## Step 4 – Orchestration Loop

- Build `simulation.py` to coordinate personas, stations, and bikes without embedding domain rules directly.
- Ensure the loop emits summaries (rides fulfilled, shortages) for future visualization hooks.

## Step 5 – Documentation & Examples
- Update `README.md` with a module-by-module overview and describe how to run a sample scenario.
- Add `examples/basic_day.py` that stitches the modules together for a single simulated day, plus a matching test to guard the example.

## Open Questions
- Where do initial station/bike counts come from? (constants vs. external CSV)
- What outputs should persist after a run? (console metrics, JSON log, plots)

Define core entities in stations.py, bikes.py, and dataclasses for trips/demand, mirrored by tests/test_stations.py.
Implement persona behaviors in personas.py with small allocation/scheduling helpers plus tests/test_personas.py.
Model routing/time progression utilities in routes.py and validate via tests/test_routes.py.
Build the orchestrating loop in simulation.py to coordinate modules, with scenario coverage in tests/test_simulation.py.
Document architecture and add a runnable walkthrough in README.md and examples/basic_day.py aligning with modules.
Further Considerations
Demand data source? Option A static constants / Option B CSV input / Option C CLI parameters
Output focus? Option A textual metrics / Option B plotted timelines / Option C persisted logs