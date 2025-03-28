from datetime import datetime
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain.entities.event import EventDM
from backend.infrustructure.models.event import Event
from backend.infrustructure.repositories.event import EventRepository

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def event_repo(session: AsyncSession) -> EventRepository:
    return EventRepository(session=session)


async def test_save_event(session: AsyncSession, event_repo: EventRepository) -> None:
    event_dm = EventDM(
        uuid=str(uuid4()),
        address='TLxMgDJhiHHQMs6NJrk5THWpdjDEuFQdqw',
        created_at=datetime.now(),
    )
    await event_repo.save(event=event_dm)

    result = await session.execute(select(Event).where(Event.uuid == event_dm.uuid))
    rows = result.fetchall()
    assert len(rows) == 1
    event = rows[0][0]
    assert event.address == event_dm.address
    assert event.created_at == event_dm.created_at
