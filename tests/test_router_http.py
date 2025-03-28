from collections.abc import AsyncIterator
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from dishka import AnyOf, AsyncContainer, Provider, Scope, make_async_container, provide
from dishka.integrations import fastapi as fastapi_integration
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy.exceptions import AddressNotFound

from backend.application import interfaces
from backend.config import Config
from backend.infrustructure.models.event import Event
from backend.infrustructure.services.trx_client import TrxClient
from backend.ioc import ApplicationProvider, InfrastructureProvider
from backend.presentation.api.exceptions_mapping import EXCEPTIONS_MAPPING
from backend.presentation.api.routers import router


@pytest.fixture
def mock_provider(session: AsyncSession) -> Provider:
    class MockProvider(InfrastructureProvider, ApplicationProvider):
        @provide(scope=Scope.REQUEST)
        async def get_session(self) -> AnyOf[AsyncSession, interfaces.DBSession]:
            return session

        @provide(scope=Scope.REQUEST)
        async def get_trx_client(self) -> interfaces.TrxClient:
            mock_async_tron = AsyncMock()

            mock_async_tron.get_account.return_value = {'balance': 10_000_000}
            mock_async_tron.get_account_resource.return_value = {
                'freeNetLimit': 500,
                'TotalEnergyLimit': 250,
            }

            return TrxClient(client=mock_async_tron)

    return MockProvider()


@pytest.fixture
def not_found_provider(session: AsyncSession) -> Provider:
    class NotFoundProvider(InfrastructureProvider, ApplicationProvider):
        @provide(scope=Scope.REQUEST)
        async def get_session(self) -> AnyOf[AsyncSession, interfaces.DBSession]:
            return session

        @provide(scope=Scope.REQUEST)
        async def get_trx_client(self) -> interfaces.TrxClient:
            mock_async_tron = AsyncMock()
            mock_async_tron.get_account.side_effect = AddressNotFound
            mock_async_tron.get_account_resource.side_effect = AddressNotFound
            return TrxClient(client=mock_async_tron)

    return NotFoundProvider()


@pytest.fixture
def container(mock_provider: Provider) -> AsyncContainer:
    return make_async_container(mock_provider, context={Config: MagicMock})


@pytest.fixture
def not_found_container(not_found_provider: Provider) -> AsyncContainer:
    return make_async_container(not_found_provider, context={Config: MagicMock()})


@pytest.fixture
async def client(container: AsyncContainer) -> AsyncIterator[AsyncClient]:
    app = FastAPI(exception_handlers=EXCEPTIONS_MAPPING)
    app.include_router(router)
    fastapi_integration.setup_dishka(container, app)
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client


@pytest.fixture
async def not_found_client(not_found_container: AsyncContainer) -> AsyncIterator[AsyncClient]:
    app = FastAPI(exception_handlers=EXCEPTIONS_MAPPING)
    app.include_router(router)
    fastapi_integration.setup_dishka(not_found_container, app)
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client


async def test_get_events(session: AsyncSession, client: AsyncClient) -> None:
    uuid = str(uuid4())
    address = 'TLxMgDJhiHHQMs6NJrk5THWpdjDEuFQdqw'
    created_at = datetime.now()

    session.add(Event(uuid=uuid, address=address, created_at=created_at))
    await session.flush()

    result = await client.get(url='/api/events', params={'page': 1, 'page_size': 1})
    assert result.status_code == 200
    print(result.json())
    assert result.json()['events'][0]['id'] == uuid
    assert result.json()['events'][0]['address'] == address
    assert result.json()['events'][0]['created_at'] == created_at.isoformat()


async def test_get_wallet_details(session: AsyncSession, client: AsyncClient) -> None:
    address = 'TLxMgDJhiHHQMs6NJrk5THWpdjDEuFQdqw'
    result = await client.post(url='/api/wallet', params={'address': address})
    assert result.status_code == 200
    assert result.json()['address'] == address
    assert result.json()['balance'] == '10'
    assert result.json()['bandwidth'] == '500'
    assert result.json()['energy'] == '250'


async def test_get_wallet_details_not_found(not_found_client: AsyncClient):
    address = 'nonexistent-wallet-address'
    result = await not_found_client.post(url='/api/wallet', params={'address': address})
    assert result.status_code == 404
    assert result.json()['detail'] == 'Wallet not found on chain'
