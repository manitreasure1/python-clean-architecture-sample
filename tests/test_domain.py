import pytest
from src.domain import Booking, Resource, BookingId, ResourceId, StudentId, TimeSlot, BookingException, ResourceException, TimeSlotException
from datetime import datetime, timedelta
from uuid import uuid4


_id = uuid4()


# region Booking
def test_booking_fails_if_duration_beyond_4hrs():
    with pytest.raises(BookingException):
        Booking.create(
            booking_id=BookingId(_id),
            resource_id=ResourceId(_id),
            student_id=StudentId(_id),
            timeslot=TimeSlot(
                datetime.now() + timedelta(hours=2), datetime.now() + timedelta(hours=7)
            ),
        )


def test_no_overlap_when_intervals_are_apart():
    a = TimeSlot(
        start=datetime.now(),
        end=datetime.now() + timedelta(hours=2),
    )
    b = TimeSlot(
        start=datetime.now() + timedelta(hours=2),
        end=datetime.now() + timedelta(hours=4),
    )
    assert a.overlaps(b) is False


def test_no_overlap_when_touching_edges():
    a = TimeSlot(
        start=datetime.now(),
        end=datetime.now() + timedelta(hours=2),
    )
    b = TimeSlot(
        start=datetime.now() + timedelta(hours=2),
        end=datetime.now() + timedelta(hours=4),
    )
    assert not a.overlaps(b)


def test_overlap_is_symmetric():
    a = TimeSlot(
        start=datetime.now(),
        end=datetime.now() + timedelta(hours=2),
    )
    b = TimeSlot(
        start=datetime.now() + timedelta(hours=1),
        end=datetime.now() + timedelta(hours=3),
    )
    assert a.overlaps(b) == b.overlaps(a)


def test_timeslot_end_before_start_raises():
    with pytest.raises(TimeSlotException) as exc_info:
        TimeSlot(start=datetime.now(), end=datetime.now())
        assert "End time must be after start time" in str(exc_info.value)


# region Resource
def test_resource_book_capacity_raises():
    with pytest.raises(ResourceException) as exc_info:
        Resource(
            resource_id=ResourceId(_id),
            name="Auditoruim",
            type="room",
            capacity=45,
            status="pending",
        )
        assert "Capacity must not exceed 40" in str(exc_info.value)


def test_resource_multi_booking_success():
    resource = Resource(
        resource_id=ResourceId(_id),
        name="Auditoruim",
        type="room",
        capacity=12,
        status="pending",
    )
    booking_a = Booking(
        booking_id=BookingId(_id),
        resource_id=resource.resource_id,
        student_id=StudentId(_id),
        timeslot=TimeSlot(datetime.now(), datetime.now() + timedelta(hours=3)),
        status="pending",
    )
    booking_b = Booking(
        booking_id=BookingId(_id),
        resource_id=resource.resource_id,
        student_id=StudentId(_id),
        timeslot=TimeSlot(
            datetime.now() + timedelta(hours=3), datetime.now() + timedelta(hours=6)
        ),
        status="pending",
    )
    resource.add_booking(booking_a)
    resource.add_booking(booking_b)


def test_resource_add_booking_raises():
    resource = Resource(
        resource_id=ResourceId(_id),
        name="Auditoruim",
        type="room",
        capacity=15,
        status="pending",
    )
    a = Booking(
        booking_id=BookingId(_id),
        resource_id=ResourceId(_id),
        student_id=StudentId(_id),
        timeslot=TimeSlot(
            datetime.now() + timedelta(hours=2), datetime.now() + timedelta(hours=7)
        ),
        status="confirmed",
    )
    b = Booking(
        booking_id=BookingId(_id),
        resource_id=ResourceId(_id),
        student_id=StudentId(_id),
        timeslot=TimeSlot(
            datetime.now() + timedelta(hours=3), datetime.now() + timedelta(hours=8)
        ),
        status="pending",
    )

    with pytest.raises(ResourceException):
        resource.add_booking(a)
        resource.add_booking(b)
