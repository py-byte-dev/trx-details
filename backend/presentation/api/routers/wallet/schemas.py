from pydantic import BaseModel


class TronWalletInfoResponseSchema(BaseModel):
    address: str
    balance: str
    bandwidth: str
    energy: str
