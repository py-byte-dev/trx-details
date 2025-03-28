from backend.application.exceptions.base import BaseApplicationError


class WalletNotFoundError(BaseApplicationError):
    def __init__(self):
        super().__init__('Wallet not found on chain')
