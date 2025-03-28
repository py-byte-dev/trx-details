from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from backend.application.use_cases.event import GetEventsInteractor
from backend.presentation.api.routers.event.schemas import EventResponseSchema, EventsResponseSchema

router = APIRouter(
    prefix='/events',
    route_class=DishkaRoute,
    tags=['wallet'],
)


@router.get('', response_model=EventsResponseSchema)
async def get_all_events(
    page: int,
    page_size: int,
    interactor: FromDishka[GetEventsInteractor],
):
    paginated_data = await interactor(page=page, page_size=page_size)

    return EventsResponseSchema(
        total=paginated_data.total,
        size=paginated_data.size,
        events=[
            EventResponseSchema(
                id=requests.uuid,
                address=requests.address,
                created_at=requests.created_at,
            )
            for requests in paginated_data.items
        ],
    )
