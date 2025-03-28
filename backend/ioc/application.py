from datetime import UTC, datetime
from uuid import uuid4

from dishka import Provider, Scope, from_context, provide

from backend.application import interfaces
from backend.application.services.pagination import PaginationService
from backend.application.use_cases.event import GetEventsInteractor, NewEventInteractor
from backend.config import Config


class ApplicationProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> interfaces.UUIDGenerator:
        return uuid4

    @provide(scope=Scope.APP)
    def generate_current_dt(self) -> interfaces.IGenerateCurrentDT:
        return lambda: datetime.now(UTC)

    get_events_interactor = provide(GetEventsInteractor, scope=Scope.REQUEST)
    new_event_interactor = provide(NewEventInteractor, scope=Scope.REQUEST)

    pagination_service = provide(PaginationService, scope=Scope.REQUEST)
