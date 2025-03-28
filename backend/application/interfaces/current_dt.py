from datetime import datetime
from typing import Protocol


class IGenerateCurrentDT(Protocol):
    def __call__(self) -> datetime: ...
