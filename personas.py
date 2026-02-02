"""Persona demand profiles for the bike-share simulation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

COMMUTER_BATCH_INTERVAL_MINUTES = 20
"""Gap between commuter arrival waves at transit hubs."""
TOURIST_BATCH_INTERVAL_MINUTES = 30
"""Gap between tourist departures once breakfast concludes."""


@dataclass(frozen=True)
class TimeWindow:
    """Inclusive-exclusive time window expressed in minutes from midnight.

    Attributes:
        start_minute: Earliest minute the window allows.
        end_minute: Minute strictly after the window ends.
    """

    start_minute: int
    end_minute: int

    def __post_init__(self) -> None:
        if self.start_minute < 0 or self.end_minute < 0:
            raise ValueError("TimeWindow bounds must be non-negative")
        if self.end_minute <= self.start_minute:
            raise ValueError("end_minute must be greater than start_minute")


@dataclass(frozen=True)
class RiderDemandProfile:
    """Demand description for a single rider persona.

    Attributes:
        persona: Short label used across reports and logs.
        departure_window: When riders begin trips.
        dwell_range_minutes: Low/high bounds for time spent away before returning.
        batch_interval_minutes: Minutes between rider arrival batches.
    """

    persona: str
    departure_window: TimeWindow
    dwell_range_minutes: Tuple[int, int]
    batch_interval_minutes: int

    def __post_init__(self) -> None:
        if not self.persona:
            raise ValueError("persona must be a non-empty string")
        low, high = self.dwell_range_minutes
        if low <= 0 or high <= 0:
            raise ValueError("dwell_range_minutes values must be positive")
        if high < low:
            raise ValueError("dwell_range_minutes upper bound must exceed lower bound")
        if self.batch_interval_minutes <= 0:
            raise ValueError("batch_interval_minutes must be positive")


def minutes_since_midnight(hours: int, minutes: int = 0) -> int:
    """Convert hour/minute pairs into minutes after midnight.

    Args:
        hours: Hour component using 24-hour time.
        minutes: Minute component of the timestamp.

    Returns:
        Integer minute count since midnight.
    """
    if hours < 0 or minutes < 0:
        raise ValueError("Time components must be non-negative")
    if minutes >= 60:
        raise ValueError("minutes must be less than 60")
    return hours * 60 + minutes


def create_commuter_profile() -> RiderDemandProfile:
    """Return the default commuter demand profile described in the README.

    Returns:
        RiderDemandProfile configured for commuter behaviors.
    """
    departure_window = TimeWindow(
        start_minute=minutes_since_midnight(7),
        end_minute=minutes_since_midnight(10),
    )
    dwell_range = (6 * 60, 9 * 60)
    return RiderDemandProfile(
        persona="commuter",
        departure_window=departure_window,
        dwell_range_minutes=dwell_range,
        batch_interval_minutes=COMMUTER_BATCH_INTERVAL_MINUTES,
    )


def create_tourist_profile() -> RiderDemandProfile:
    """Return the default tourist demand profile described in the README.

    Returns:
        RiderDemandProfile configured for tourist behaviors.
    """
    departure_window = TimeWindow(
        start_minute=minutes_since_midnight(7),
        end_minute=minutes_since_midnight(9),
    )
    dwell_range = (60, 180)
    return RiderDemandProfile(
        persona="tourist",
        departure_window=departure_window,
        dwell_range_minutes=dwell_range,
        batch_interval_minutes=TOURIST_BATCH_INTERVAL_MINUTES,
    )
