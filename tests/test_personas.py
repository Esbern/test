"""Unit tests for personas module."""

import pytest

from personas import (
    RiderDemandProfile,
    TimeWindow,
    create_commuter_profile,
    create_tourist_profile,
    minutes_since_midnight,
)


def test_minutes_since_midnight_converts_values() -> None:
    assert minutes_since_midnight(7, 30) == 450


def test_commuter_profile_uses_expected_windows() -> None:
    profile = create_commuter_profile()
    assert isinstance(profile.departure_window, TimeWindow)
    assert profile.departure_window.start_minute == 420
    assert profile.departure_window.end_minute == 600
    assert profile.dwell_range_minutes == (360, 540)


def test_tourist_profile_has_shorter_dwell() -> None:
    profile = create_tourist_profile()
    assert profile.dwell_range_minutes == (60, 180)


def test_rider_demand_profile_rejects_invalid_dwell_range() -> None:
    window = TimeWindow(start_minute=0, end_minute=60)
    with pytest.raises(ValueError):
        RiderDemandProfile(
            persona="invalid",
            departure_window=window,
            dwell_range_minutes=(120, 60),
            batch_interval_minutes=15,
        )