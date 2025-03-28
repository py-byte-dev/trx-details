from collections.abc import AsyncIterable

from dishka import AnyOf, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from tronpy import AsyncTron
from tronpy.defaults import CONF_MAINNET
from tronpy.providers import AsyncHTTPProvider

from backend.application import interfaces
from backend.config import Config
from backend.infrustructure.repositories.event import EventRepository
from backend.infrustructure.repositories.wallet import WalletRepository
from backend.infrustructure.services.trx_client import TrxClient


class InfrastructureProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=interfaces.TrxClient)
    async def get_trx_client(self, config: Config) -> TrxClient:
        provider = AsyncHTTPProvider(endpoint_uri=CONF_MAINNET, api_key=config.trx.api_key)
        client = AsyncTron(provider=provider)

        return TrxClient(client=client)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        database_uri = f'postgresql+psycopg://{config.pg.user}:{config.pg.password}@{config.pg.host}:{config.pg.port}/{config.pg.db}'

        engine = create_async_engine(
            database_uri,
            pool_size=15,
            max_overflow=15,
            connect_args={
                'connect_timeout': 5,
            },
        )
        return async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[
        AnyOf[
            AsyncSession,
            interfaces.DBSession,
        ]
    ]:
        async with session_maker() as session:
            yield session

    event_repo = provide(
        EventRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[interfaces.EventReader, interfaces.EventSaver],
    )

    wallet_repo = provide(
        WalletRepository,
        scope=Scope.REQUEST,
        provides=interfaces.WalletReader,
    )
