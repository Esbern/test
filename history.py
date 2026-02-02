"""Historical snapshots for bike-share simulation metrics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence, Tuple

from bikes import BikeInventorySnapshot

StateInput = Mapping[str, int] | Iterable[tuple[str, int]]
"""Accepted rider state inputs for history recording."""


@dataclass(frozen=True)
class StateCount:
    """Immutable label/count pair for rider state tallies.

    Attributes:
        label: Name of the rider state (e.g., "waiting", "riding").
        count: Number of riders in the state.
    """

    label: str
    count: int

    def __post_init__(self) -> None:
        if not self.label:
            raise ValueError("label must be a non-empty string")
        if self.count < 0:
            raise ValueError("count must be non-negative")


@dataclass(frozen=True)
class StationStatus:
    """Immutable snapshot of a station's bike availability.

    Attributes:
        station_id: Identifier of the station represented.
        bikes_available: Number of bikes currently docked.
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


@dataclass(frozen=True)
class SystemSnapshot:
    """Aggregated counts for riders and stations at a point in time.

    Attributes:
        minute: Minutes since midnight when the snapshot was captured.
        rider_states: Rider state counts stored as immutable pairs.
        station_status: Station availability at the same timestamp.
    """

    minute: int
    rider_states: Tuple[StateCount, ...]
    station_status: Tuple[StationStatus, ...]

    def __post_init__(self) -> None:
        if self.minute < 0:
            raise ValueError("minute must be non-negative")


class HistoryRecorder:
    """Collects snapshots for later plotting or analysis.

    The recorder is intentionally lightweight so notebook experiments can
    append data as they iterate on scenario assumptions.
    """

    def __init__(self) -> None:
        self._snapshots: list[SystemSnapshot] = []

    def record(
        self,
        minute: int,
        rider_states: StateInput,
        station_snapshots: Iterable[BikeInventorySnapshot],
    ) -> SystemSnapshot:
        """Store a new snapshot of rider and station counts.

        Args:
            minute: Minutes since midnight for the snapshot.
            rider_states: Mapping or iterable describing riders per state.
            station_snapshots: Inventory snapshots for each station being tracked.

        Returns:
            The immutable SystemSnapshot that was recorded.
        """

        normalized_states = _normalize_state_counts(rider_states)
        station_status = tuple(
            StationStatus(
                station_id=snapshot.station_id,
                bikes_available=snapshot.bikes_available,
                docks_available=snapshot.docks_available,
            )
            for snapshot in station_snapshots
        )
        snapshot = SystemSnapshot(
            minute=minute,
            rider_states=normalized_states,
            station_status=station_status,
        )
        self._snapshots.append(snapshot)
        return snapshot

    def snapshots(self) -> Tuple[SystemSnapshot, ...]:
        """Return all recorded snapshots in chronological order."""

        return tuple(self._snapshots)

    def rider_state_series(self, state_label: str) -> list[tuple[int, int]]:
        """Return (minute, count) pairs for a specific rider state label."""

        if not state_label:
            raise ValueError("state_label must be a non-empty string")
        series: list[tuple[int, int]] = []
        for snapshot in self._snapshots:
            count = next((state.count for state in snapshot.rider_states if state.label == state_label), 0)
            series.append((snapshot.minute, count))
        return series

    def station_bike_series(self, station_id: str) -> list[tuple[int, int]]:
        """Return (minute, bikes_available) pairs for a station."""

        if not station_id:
            raise ValueError("station_id must be a non-empty string")
        series: list[tuple[int, int]] = []
        for snapshot in self._snapshots:
            bikes = next(
                (status.bikes_available for status in snapshot.station_status if status.station_id == station_id),
                0,
            )
            series.append((snapshot.minute, bikes))
        return series


def _normalize_state_counts(rider_states: StateInput) -> Tuple[StateCount, ...]:
    """Convert arbitrary rider state inputs into StateCount tuples."""

    if isinstance(rider_states, Mapping):
        items: Sequence[tuple[str, int]] = tuple(rider_states.items())
    else:
        items = tuple(rider_states)
    return tuple(StateCount(label=label, count=count) for label, count in items)
