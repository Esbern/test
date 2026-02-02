"""Bike inventory snapshots and helper utilities."""

from __future__ import annotations

from dataclasses import dataclass

from stations import StationProfile

DEFAULT_BIKE_BUFFER = 2
"""Minimum number of bikes to leave undocked for maintenance rotation."""


@dataclass(frozen=True)
class BikeInventorySnapshot:
    """Immutable capture of bikes and docks at a station.

    Attributes:
        station_id: Identifier of the station represented.
        bikes_available: Bikes currently docked and ready.
        docks_available: Empty docks available for returns.
    """

    station_id: str
    bikes_available: int
    docks_available: int

    def __post_init__(self) -> None:
        if not self.station_id:
            raise ValueError("station_id must be a non-empty string")
        if self.bikes_available < 0:
            raise ValueError("bikes_available must be non-negative")
        if self.docks_available < 0:
            raise ValueError("docks_available must be non-negative")


def derive_inventory(profile: StationProfile, docked_bikes: int) -> BikeInventorySnapshot:
    """Create an inventory snapshot based on a station profile.

    Args:
        profile: Station metadata driving dock capacity.
        docked_bikes: Number of bikes currently parked at the station.

    Returns:
        Inventory snapshot describing bikes and open docks.
    """
    if docked_bikes < 0:
        raise ValueError("docked_bikes must be non-negative")
    if docked_bikes > profile.capacity:
        raise ValueError("docked_bikes cannot exceed station capacity")
    docks_available = profile.capacity - docked_bikes
    return BikeInventorySnapshot(
        station_id=profile.identifier,
        bikes_available=docked_bikes,
        docks_available=docks_available,
    )


def can_release_bike(snapshot: BikeInventorySnapshot, requested_bikes: int) -> bool:
    """Return True when the snapshot can satisfy the requested bikes.

    Args:
        snapshot: Inventory reference for a single station.
        requested_bikes: Number of bikes the rider wants to take.

    Returns:
        True when fulfilling the request keeps the maintenance buffer intact.
    """
    if requested_bikes < 0:
        raise ValueError("requested_bikes must be non-negative")
    return snapshot.bikes_available - requested_bikes >= DEFAULT_BIKE_BUFFER
