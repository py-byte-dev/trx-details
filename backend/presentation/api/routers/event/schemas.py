from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EventResponseSchema(BaseModel):
    id: UUID
    address: str
    created_at: datetime


class EventsResponseSchema(BaseModel):
    total: int
    size: int
    events: list[EventResponseSchema]
