from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = 'events'

    uuid: Mapped[str] = mapped_column(
        'uuid',
        sa.Uuid,
        primary_key=True,
    )
    address: Mapped[str]
    created_at: Mapped[datetime]
