from abc import ABC, abstractmethod


class IBookingRepository(ABC):

    @abstractmethod
    def add(self):...

    @abstractmethod
    def find_by_id(self):...

    @abstractmethod
    def find_overlap(self): ...

    @abstractmethod
    def get_pendings(self): ...

    @abstractmethod
    def check_status(self): ...

    @abstractmethod
    def update_booking_status(self): ...
