from sqlalchemy import (
    String,
    Float,
    DateTime,
    Date,
    Time,
    BigInteger,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from geopy.geocoders import Nominatim

from datetime import date, time

from database.base import Base


class Profile(Base):
    __tablename__ = 'Profile'

    id: Mapped[BigInteger] = mapped_column(
        BigInteger, unique=True, index=True, nullable=False, primary_key=True, autoincrement=True
    )

    user_id: Mapped[BigInteger] = mapped_column(
        BigInteger, nullable=False
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

    location_timezone: Mapped[str] = mapped_column(
        String, nullable=False
    )

    def get_location(self):
        """Fetch location description using latitude and longitude."""
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse((self.location_latitude, self.location_longitude), language='en')
        return location.address if location else "Location not found"

    def __doc__(self):
        return f'{self.__class__.__name__}({self.id})'

    def __str__(self):
        return (f"Profile Title: {self.title}\n"
                f"Birth Date: {self.birth_date.strftime('%Y-%m-%d')}\n"
                f"Birth Time: {self.birth_time.strftime('%H:%M')}\n"
                f"Birth Timezone: {self.birth_timezone}\n"
                f"Birth Latitude: {self.birth_latitude}\n"
                f"Birth Longitude: {self.birth_longitude}\n"
                f"Location Latitude: {self.location_latitude}\n"
                f"Location Longitude: {self.location_longitude}\n"
                f"Location Timezone: {self.location_timezone}\n")
                # f"Location Description: {self.get_location()}\n") 