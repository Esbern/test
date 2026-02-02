# Bikeshare Simulation

This project simulates a bike-share system with two rider personas.

## Modules

- `stations.py` defines immutable station profiles plus helpers to compute open docks or detect overflow.
- `bikes.py` captures station-level inventory snapshots and enforces a small maintenance buffer when riders request bikes.
- `personas.py` stores commuter and tourist demand profiles (time windows, dwell ranges, batch sizes) so later steps can turn them into trips.
- `history.py` records rider-state and station availability snapshots so you can build plots or dashboards from the simulation timeline.

## Commuters

- Arrive at major transit hubs between 07:00–10:00 in 20-minute waves.
- Pick up a nearby bike and ride to an office-area station.
- After 6–9 hours they seek another bike and return to the origin station.

## Tourists

- Start from hotels around 07:00–09:00 after a 30–60 minute breakfast.
- Ride to a tourist attraction, stay 1–3 hours, then pick a new destination.
- If it is past 17:00 they return to the hotel instead of another attraction.

## Notebooks

- `notebooks/history_playground.ipynb` lets you tweak manual scenarios, inspect the resulting history, and prototype plots without needing the full simulation loop.

## Run in Colab

1. Install the Google Colab extension in VS Code and connect it to your Google account.
2. Open `notebooks/history_playground.ipynb` via the command palette (`Colab: Open Notebook`), then choose the hosted runtime you prefer (CPU/GPU).
3. In a new cell at the top, run `%pip install -r requirements.txt` so Colab matches the local dependencies.
4. Execute the setup cell that defines `station_profiles` and `run_manual_scenario()`, then iterate on the scenario rows or plot cell to visualize rider states and station availability over time.