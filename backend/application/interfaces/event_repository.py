from abc import abstractmethod
from collections.abc import Collection
from typing import Protocol

from backend.domain.entities.event import EventDM


class EventReader(Protocol):
    @abstractmethod
    async def get_all(self) -> Collection[EventDM]: ...


class EventSaver(Protocol):
    @abstractmethod
    async def save(self, event: EventDM) -> None: ...
