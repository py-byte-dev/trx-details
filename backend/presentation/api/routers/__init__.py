from fastapi import APIRouter

from backend.presentation.api.routers.event.route import router as event_router
from backend.presentation.api.routers.wallet.route import router as wallet_router

router = APIRouter(
    prefix='/api',
)

router.include_router(event_router)
router.include_router(wallet_router)
