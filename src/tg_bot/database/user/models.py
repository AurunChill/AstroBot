from sqlalchemy import (
    Enum as SAEnum,
    DateTime,
    BigInteger,
    String
)
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime
from typing import Optional
from enum import Enum

from database.base import Base


class Subscription(Enum):
    FOREVER = 'forever'
    MONTHLY = 'monthly'
    FREELY = 'freely'


class User(Base):
    __tablename__ = 'User'

    id: Mapped[BigInteger] = mapped_column(
        BigInteger, unique=True, index=True, nullable=False, primary_key=True, autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String, nullable=False
    )

    current_profile_id: Mapped[Optional[BigInteger]] = mapped_column(
        BigInteger,
        nullable=True,
        unique=True,
    )

    subscription: Mapped[Subscription] = mapped_column(
        SAEnum(Subscription), nullable=False, default=Subscription.FREELY
    )

    subscription_expiration_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, default=None
    )

    def __doc__(self):
        return f'{self.__class__.__name__}({self.id})'

    def __str__(self):
        return f'User({self.id})'