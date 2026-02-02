"""Unit tests for stations module."""

import pytest

from stations import StationProfile, available_docks, is_over_capacity


def test_station_profile_uses_default_capacity() -> None:
    profile = StationProfile(identifier="hub-1", name="Transit Hub")
    assert profile.capacity == 20


def test_available_docks_reduces_capacity() -> None:
    profile = StationProfile(identifier="hub-1", name="Transit Hub", capacity=30)
    assert available_docks(profile, docked_bikes=12) == 18


def test_is_over_capacity_detects_overflow() -> None:
    profile = StationProfile(identifier="hub-1", name="Transit Hub", capacity=8)
    assert is_over_capacity(profile, docked_bikes=10) is True


def test_station_profile_rejects_empty_names() -> None:
    with pytest.raises(ValueError):
        StationProfile(identifier="", name="Invalid")