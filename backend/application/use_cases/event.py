from backend.application import interfaces
from backend.application.services.pagination import PaginationService
from backend.domain.entities.event import EventDM
from backend.domain.entities.pagination import Pagination
from backend.domain.entities.wallet import TronWalletDM


class GetEventsInteractor:
    def __init__(
        self,
        reader: interfaces.EventReader,
        pagination: PaginationService,
    ):
        self._reader = reader
        self._pagination = pagination

    async def __call__(self, page: int, page_size: int) -> Pagination[EventDM]:
        items = await self._reader.get_all()
        return self._pagination.create_page(page=page, page_size=page_size, items=items)


class NewEventInteractor:
    def __init__(
        self,
        db_session: interfaces.DBSession,
        event_saver: interfaces.EventSaver,
        wallet_reader: interfaces.WalletReader,
        uuid_generator: interfaces.UUIDGenerator,
        current_dt: interfaces.IGenerateCurrentDT,
    ):
        self._db_session = db_session
        self._event_saver = event_saver
        self._wallet_reader = wallet_reader
        self._uuid_generator = uuid_generator
        self._current_dt = current_dt

    async def __call__(self, address: str) -> TronWalletDM:
        wallet_details = await self._wallet_reader.get_wallet_info(address=address)

        event = EventDM(
            uuid=self._uuid_generator(),
            address=address,
            created_at=self._current_dt(),
        )
        await self._event_saver.save(event=event)
        await self._db_session.commit()

        return wallet_details
