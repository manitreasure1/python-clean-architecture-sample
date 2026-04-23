from dataclasses import dataclass, field
from typing import Literal
from ..value_objects import ResourceId
from ..errors import ResourceException
from .booking import Booking


@dataclass
class Resource:
    resource_id: ResourceId
    name: str
    type: Literal["room", "Lab", "equipment"]
    capacity: int
    status: Literal[
        "pending",
        "in_use",
    ]
    bookings: list[Booking] = field(default_factory=list[Booking])

    def __post_init__(self):
        if self.capacity > 40:
            raise ResourceException("Capacity must not exceed 40")

    def add_booking(self, booking: Booking):
        for existing in self.bookings:
            if existing.timeslot.overlaps(booking.timeslot):
                raise ResourceException("Booking conflict")
        self.bookings.append(booking)
