from datetime import datetime, timedelta
from typing import NewType
from uuid import UUID
from dataclasses import dataclass
from .errors import TimeSlotException

# region value objects (ID's)

ResourceId = NewType("ResourceId", UUID)
BookingId = NewType("BookingId", UUID)
StudentId = NewType("StudentId", UUID)


@dataclass(frozen=True)
class TimeSlot:
    start: datetime
    end: datetime

    def __post_init__(self):
        if self.end <= self.start:
            raise TimeSlotException("End time must be after start time")

    def duration(self) -> timedelta:
        return self.end - self.start

    def overlaps(self, other: "TimeSlot") -> bool:
        return self.start < other.end and other.start < self.end

