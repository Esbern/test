"""Unit tests for bikes module."""

import pytest

from bikes import BikeInventorySnapshot, can_release_bike, derive_inventory
from stations import StationProfile


def test_derive_inventory_reflects_station_capacity() -> None:
    profile = StationProfile(identifier="office-1", name="Office Plaza", capacity=15)
    snapshot = derive_inventory(profile, docked_bikes=9)
    assert snapshot.station_id == "office-1"
    assert snapshot.bikes_available == 9
    assert snapshot.docks_available == 6


def test_can_release_bike_respects_buffer() -> None:
    snapshot = BikeInventorySnapshot(station_id="hub-1", bikes_available=6, docks_available=4)
    assert can_release_bike(snapshot, requested_bikes=3) is True
    assert can_release_bike(snapshot, requested_bikes=5) is False


def test_derive_inventory_rejects_invalid_counts() -> None:
    profile = StationProfile(identifier="hub-1", name="Transit Hub", capacity=10)
    with pytest.raises(ValueError):
        derive_inventory(profile, docked_bikes=12)