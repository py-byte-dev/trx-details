from dataclasses import dataclass, field
from os import environ as env


@dataclass(slots=True)
class PgConfig:
    db: str = field(default_factory=lambda: env.get('POSTGRES_DB').strip())
    host: str = field(default_factory=lambda: env.get('POSTGRES_HOST').strip())
    port: int = field(default_factory=lambda: int(env.get('POSTGRES_PORT').strip()))
    user: str = field(default_factory=lambda: env.get('POSTGRES_USER').strip())
    password: str = field(default_factory=lambda: env.get('POSTGRES_PASSWORD').strip())


@dataclass
class TrxConfig:
    api_key: str = field(default_factory=lambda: env.get('TRONGRID_API_KEY').strip())


@dataclass(slots=True)
class Config:
    pg: PgConfig = field(default_factory=PgConfig)
    trx: TrxConfig = field(default_factory=TrxConfig)
