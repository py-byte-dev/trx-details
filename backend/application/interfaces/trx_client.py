from abc import abstractmethod
from typing import Protocol

from backend.application.dto.address_details import WalletBalanceDTO, WalletResourcesDTO


class TrxClient(Protocol):
    @abstractmethod
    async def get_account_balance(self, address: str) -> WalletBalanceDTO: ...

    @abstractmethod
    async def get_account_resources(self, address: str) -> WalletResourcesDTO: ...
