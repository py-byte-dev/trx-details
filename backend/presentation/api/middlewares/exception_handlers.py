from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette import status


async def wallet_not_found_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'detail': str(exc)},
    )
