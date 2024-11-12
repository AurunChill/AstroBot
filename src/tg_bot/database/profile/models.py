from datetime import date, time

from sqlalchemy import String, Float, DateTime, Date, Time, BigInteger, func
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Profile(Base):
    __tablename__ = 'Profile'

    id: Mapped[BigInteger] = mapped_column(
        BigInteger, unique=True, index=True, nullable=False, primary_key=True, autoincrement=True
    )
    
    user_id: Mapped[BigInteger] = mapped_column(
        BigInteger, nullable=False
    )

    user_name: Mapped[str] = mapped_column(
        String, nullable=False
    )

    creation_date: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now()
    )

    title: Mapped[str] = mapped_column(
        String, nullable=False
    )

    birth_date: Mapped[date] = mapped_column(
        Date, nullable=False
    )

    birth_time: Mapped[Time] = mapped_column(
        Time, default=time(0, 0)
    )

    birth_timezone: Mapped[str] = mapped_column(
        String, nullable=False
    )

    birth_latitude: Mapped[float] = mapped_column(
        Float, nullable=False
    )

    birth_longitude: Mapped[float] = mapped_column(
        Float, nullable=False
    )

    location_latitude: Mapped[float] = mapped_column(
        Float, nullable=False
    )

    location_longitude: Mapped[float] = mapped_column(
        Float, nullable=False
    )

    def __doc__(self):
        return f'{__class__.__name__}({self.id})'

    def __str__(self):
        return f'({self.id})'