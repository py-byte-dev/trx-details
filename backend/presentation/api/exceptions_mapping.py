from backend.application import exceptions
from backend.presentation.api.middlewares import exception_handlers

EXCEPTIONS_MAPPING = {
    exceptions.WalletNotFoundError: exception_handlers.wallet_not_found_exception_handler,
}
