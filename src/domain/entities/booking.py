
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Literal
from ..value_objects import BookingId, ResourceId, StudentId, TimeSlot
from ..errors import BookingException


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
