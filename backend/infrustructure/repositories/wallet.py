import asyncio

from backend.application import interfaces
from backend.domain.entities.wallet import TronWalletDM


class WalletRepository(
    interfaces.WalletReader,
):
    def __init__(
        self,
        trx_client: interfaces.TrxClient,
    ):
        self._trx_client = trx_client

    async def get_wallet_info(self, address: str) -> TronWalletDM:
        tasks = [
            self._trx_client.get_account_balance(address=address),
            self._trx_client.get_account_resources(address=address),
        ]

        balance_dto, resources_dto = await asyncio.gather(*tasks)

        return TronWalletDM(
            address=address,
            balance=balance_dto.balance,
            energy=resources_dto.energy,
            bandwidth=resources_dto.bandwidth,
        )
