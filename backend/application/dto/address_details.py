from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class WalletBalanceDTO:
    balance: Decimal


@dataclass(slots=True)
class WalletResourcesDTO:
    bandwidth: int
    energy: int
