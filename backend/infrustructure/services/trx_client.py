from decimal import Decimal

from tronpy import AsyncTron
from tronpy.exceptions import AddressNotFound

from backend.application import exceptions, interfaces
from backend.application.dto.address_details import WalletBalanceDTO, WalletResourcesDTO

TOKEN_UNIT = 1_000_000


class TrxClient(interfaces.TrxClient):
    def __init__(
        self,
        client: AsyncTron,
    ):
        self._client = client

    async def get_account_balance(self, address: str) -> WalletBalanceDTO:
        try:
            account = await self._client.get_account(addr=address)
            balance_sun = account.get('balance', 0)
            balance_trx = Decimal(balance_sun) / Decimal(TOKEN_UNIT)
            return WalletBalanceDTO(balance=balance_trx)
        except AddressNotFound:
            raise exceptions.WalletNotFoundError

    async def get_account_resources(self, address: str) -> WalletResourcesDTO:
        try:
            resources = await self._client.get_account_resource(addr=address)
            return WalletResourcesDTO(
                bandwidth=resources.get('freeNetLimit', 0),
                energy=resources.get('TotalEnergyLimit', 0),
            )
        except AddressNotFound:
            raise exceptions.WalletNotFoundError
