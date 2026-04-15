from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Literal
from .value_objects import BookingId, ResourceId, StudentId, TimeSlot
from .errors import ResourceException, BookingException

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
    bookings: list["Booking"] = field(default_factory=list["Booking"])
    def __post_init__(self):
        if self.capacity > 40:
            raise ResourceException("Capacity must not exceed 40")

    def add_booking(self, booking: "Booking"):
        for existing in self.bookings:
            if existing.timeslot.overlaps(booking.timeslot):
                raise ResourceException("Booking conflict")
        self.bookings.append(booking)


@dataclass
class Booking:
    booking_id: BookingId
    resource_id: ResourceId
    student_id: StudentId
    timeslot: TimeSlot
    status: Literal["pending", "confirmed", "cancelled"]

    @classmethod
    def create(
        cls,
        booking_id: BookingId,
        resource_id: ResourceId,
        student_id: StudentId,
        timeslot: TimeSlot,
    ):
        if timeslot.duration() > timedelta(hours=4):
            raise BookingException("Booking cannot exceed 4 hours")

        if timeslot.start < datetime.now() + timedelta(hours=1):
            raise BookingException("Must book at least 1 hour ahead")

        return cls(
            booking_id,
            resource_id,
            student_id,
            timeslot,
            "pending",
        )
