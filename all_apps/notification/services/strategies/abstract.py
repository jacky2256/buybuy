from abc import ABC, abstractmethod


class NotificationStrategy(ABC):
    @abstractmethod
    def send(self, user, content: str, payload: dict):
        pass
