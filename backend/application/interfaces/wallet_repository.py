from abc import abstractmethod
from typing import Protocol

from backend.domain.entities.wallet import TronWalletDM


class WalletReader(Protocol):
    @abstractmethod
    async def get_wallet_info(self, address: str) -> TronWalletDM: ...
