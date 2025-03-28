from collections.abc import Collection

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from backend.application import interfaces
from backend.domain.entities.event import EventDM


class EventRepository(
    interfaces.EventReader,
    interfaces.EventSaver,
):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self) -> Collection[EventDM]:
        query = text('SELECT uuid, address, created_at FROM events')
        result = await self._session.execute(statement=query)
        rows = result.fetchall()

        return [
            EventDM(
                uuid=row.uuid,
                address=row.address,
                created_at=row.created_at,
            )
            for row in rows
        ]

    async def save(self, event: EventDM) -> None:
        statement = text('INSERT INTO events (uuid, address, created_at) VALUES (:uuid, :wallet, :created_at)')
        await self._session.execute(
            statement=statement,
            params={
                'uuid': event.uuid,
                'wallet': event.address,
                'created_at': event.created_at,
            },
        )
