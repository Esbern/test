# Copilot Instructions

## Mission Context
- Goal: build a Python-based bike share simulation that helps a beginner learn by example.
- Codebase currently empty; every new file should teach via clarity, docstrings, and inline comments only when the logic is non-obvious.
- Prefer running notebooks through the VS Code Google Colab extension so experiments share the same hosted runtime setup.

## Coding Style
- Implement behavior through small, single-responsibility functions or classes; keep each under ~30 lines when practical.
- Prioritize readability over cleverness; favor descriptive names like `allocate_bikes_to_station()` over abbreviations.
- Each public function/class must include a concise Google-style docstring describing purpose, params, returns, and side effects.
- Keep module-level constants grouped at the top of the file with short explanatory comments when the value choice is not obvious.

## Simulation Structure Expectations
- Separate domain concepts into focused modules (e.g., `stations.py`, `bikes.py`, `routes.py`, `simulation.py`).
- Central simulation loop should orchestrate interactions between modules, not implement business rules directly.
- Use dataclasses for immutable data snapshots (trips, demand profiles) to keep constructors tidy and typed.
- Ensure the simulation emits a chronological time log (rider states, station availability) suitable for graphing state changes over time.

## Testing Discipline
- Create tests alongside code; mirror module names inside `tests/` (e.g., `tests/test_stations.py`).
- Prefer pytest-style unit tests with clear Arrange/Act/Assert sections and descriptive test names.
- When a bug is discovered, add or extend a regression test before fixing it.

## Documentation & Examples
- Update `README.md` as new capabilities appear; include sample CLI commands or script usage.
- Provide runnable examples (e.g., `examples/basic_day.py`) that highlight how modules collaborate.
- Whenever you add a new module, include a short section in the README explaining its role in the simulation.
