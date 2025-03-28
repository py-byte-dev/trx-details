from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from backend.application.use_cases.event import NewEventInteractor
from backend.presentation.api.routers.wallet.schemas import TronWalletInfoResponseSchema

router = APIRouter(
    prefix='/wallet',
    route_class=DishkaRoute,
    tags=['wallet'],
)


@router.post('', response_model=TronWalletInfoResponseSchema)
async def get_wallet_details(
    address: str,
    interactor: FromDishka[NewEventInteractor],
):
    details = await interactor(address=address)
    return TronWalletInfoResponseSchema(
        address=details.address,
        balance=str(details.balance),
        bandwidth=str(details.bandwidth),
        energy=str(details.energy),
    )
