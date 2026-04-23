from abc import ABC, abstractmethod


class INotificationService(ABC):

    @abstractmethod
    def send(self): ...