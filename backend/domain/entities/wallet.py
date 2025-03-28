from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class TronWalletDM:
    address: str
    balance: Decimal
    energy: int
    bandwidth: int
