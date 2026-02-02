"""Unit tests for history module."""

import pytest

from bikes import BikeInventorySnapshot
from history import HistoryRecorder, StationStatus, SystemSnapshot


def test_record_creates_snapshot_with_station_data() -> None:
    recorder = HistoryRecorder()
    station_snapshots = [
        BikeInventorySnapshot(station_id="hub-1", bikes_available=12, docks_available=8),
        BikeInventorySnapshot(station_id="park-1", bikes_available=5, docks_available=5),
    ]

    snapshot = recorder.record(
        minute=60,
        rider_states={"waiting": 7, "riding": 4},
        station_snapshots=station_snapshots,
    )

    assert isinstance(snapshot, SystemSnapshot)
    assert snapshot.minute == 60
    assert len(snapshot.rider_states) == 2
    assert snapshot.station_status == (
        StationStatus(station_id="hub-1", bikes_available=12, docks_available=8),
        StationStatus(station_id="park-1", bikes_available=5, docks_available=5),
    )


def test_rider_state_series_fills_missing_state() -> None:
    recorder = HistoryRecorder()
    recorder.record(
        minute=0,
        rider_states={"waiting": 5},
        station_snapshots=[BikeInventorySnapshot(station_id="hub-1", bikes_available=10, docks_available=0)],
    )
    recorder.record(
        minute=30,
        rider_states={"waiting": 2, "riding": 3},
        station_snapshots=[BikeInventorySnapshot(station_id="hub-1", bikes_available=8, docks_available=2)],
    )

    assert recorder.rider_state_series("riding") == [(0, 0), (30, 3)]


def test_station_bike_series_returns_counts() -> None:
    recorder = HistoryRecorder()
    recorder.record(
        minute=0,
        rider_states={"waiting": 1},
        station_snapshots=[
            BikeInventorySnapshot(station_id="hub-1", bikes_available=9, docks_available=1),
            BikeInventorySnapshot(station_id="park-1", bikes_available=6, docks_available=4),
        ],
    )
    recorder.record(
        minute=15,
        rider_states={"waiting": 0},
        station_snapshots=[
            BikeInventorySnapshot(station_id="hub-1", bikes_available=7, docks_available=3),
            BikeInventorySnapshot(station_id="park-1", bikes_available=5, docks_available=5),
        ],
    )

    assert recorder.station_bike_series("park-1") == [(0, 6), (15, 5)]


def test_record_rejects_negative_time() -> None:
    recorder = HistoryRecorder()
    with pytest.raises(ValueError):
        recorder.record(
            minute=-5,
            rider_states={"waiting": 1},
            station_snapshots=[BikeInventorySnapshot(station_id="hub-1", bikes_available=5, docks_available=5)],
        )
