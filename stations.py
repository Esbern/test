"""Station metadata and helper utilities for the bike-share simulation."""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_STATION_CAPACITY = 20
"""Default dock count for a mid-sized city station."""


def _validate_non_negative(value: int, field_name: str) -> None:
    """Raise ValueError when a capacity-related field is negative."""
    if value < 0:
        raise ValueError(f"{field_name} must be non-negative, got {value}")


@dataclass(frozen=True)
class StationProfile:
    """Immutable station description.

    Attributes:
        identifier: Stable station identifier used across modules.
        name: Human-readable station name for logs or dashboards.
        capacity: Total number of docks the station provides.
    """

    identifier: str
    name: str
    capacity: int = DEFAULT_STATION_CAPACITY

    def __post_init__(self) -> None:
        if not self.identifier:
            raise ValueError("identifier must be a non-empty string")
        if not self.name:
            raise ValueError("name must be a non-empty string")
        _validate_non_negative(self.capacity, "capacity")
        if self.capacity == 0:
            raise ValueError("capacity must be greater than zero")


def available_docks(profile: StationProfile, docked_bikes: int) -> int:
    """Return remaining dock slots after accounting for docked bikes.

    Args:
        profile: Station being evaluated.
        docked_bikes: Current number of bikes occupying docks.

    Returns:
        Remaining dock count for the provided station.
    """
    _validate_non_negative(docked_bikes, "docked_bikes")
    if docked_bikes > profile.capacity:
        raise ValueError("docked_bikes cannot exceed station capacity")
    return profile.capacity - docked_bikes


def is_over_capacity(profile: StationProfile, docked_bikes: int) -> bool:
    """Return True when the docked bikes exceed the station capacity.

    Args:
        profile: Station being evaluated.
        docked_bikes: Current number of bikes occupying docks.

    Returns:
        True if docked bikes exceed capacity, otherwise False.
    """
    _validate_non_negative(docked_bikes, "docked_bikes")
    return docked_bikes > profile.capacity
