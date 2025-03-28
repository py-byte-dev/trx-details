from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class EventDM:
    uuid: UUID
    address: str
    created_at: datetime
