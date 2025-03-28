from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, create_autospec

import pytest
from faker import Faker

from backend.application import interfaces
from backend.application.services.pagination import PaginationService
from backend.application.use_cases.event import GetEventsInteractor, NewEventInteractor
from backend.domain.entities.event import EventDM
from backend.domain.entities.wallet import TronWalletDM

pytestmark = pytest.mark.asyncio


@pytest.fixture
def get_events_interactor(faker: Faker) -> GetEventsInteractor:
    event_repo = create_autospec(interfaces.EventReader)
    pagination = create_autospec(PaginationService)
    return GetEventsInteractor(reader=event_repo, pagination=pagination)


async def test_get_events(get_events_interactor: GetEventsInteractor) -> None:
    await get_events_interactor(page=1, page_size=2)
    get_events_interactor._reader.get_all.assert_awaited_once()
    get_events_interactor._pagination.create_page.assert_called_once()


@pytest.fixture
def new_event_interactor(faker: Faker) -> NewEventInteractor:
    db_session = create_autospec(interfaces.DBSession)
    event_repo = create_autospec(interfaces.EventSaver)
    wallet_repo = create_autospec(interfaces.WalletReader)
    wallet_repo.get_wallet_info = AsyncMock(
        return_value=TronWalletDM(
            address='TVxoygpGTHVKGQowZMCgjxasreDFQ5kRPd',
            balance=Decimal(100),
            energy=550,
            bandwidth=500,
        ),
    )
    uuid_generator = MagicMock(return_value=faker.uuid4())
    current_dt = MagicMock(
        return_value=datetime(2025, 3, 28, 10, 7, 42, 123456),
    )

    return NewEventInteractor(
        db_session=db_session,
        event_saver=event_repo,
        wallet_reader=wallet_repo,
        uuid_generator=uuid_generator,
        current_dt=current_dt,
    )


async def test_new_event(new_event_interactor: NewEventInteractor, faker: Faker) -> None:
    address = 'TVxoygpGTHVKGQowZMCgjxasreDFQ5kRPd'
    result = await new_event_interactor(address=address)
    uuid = new_event_interactor._uuid_generator()
    created_at = new_event_interactor._current_dt()

    event = EventDM(
        uuid=uuid,
        address=address,
        created_at=created_at,
    )

    new_event_interactor._event_saver.save.assert_awaited_with(event=event)

    new_event_interactor._db_session.commit.assert_awaited_once()
    assert result.address == address
    assert result.balance == Decimal(100)
    assert result.energy == 550
    assert result.bandwidth == 500
