from enum import Enum
from sqlalchemy import String, BigInteger, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from database.base import Base


class PredictionType(Enum):
    HOROSCOPE = "horoscope"
    EVENT = "event"


class Prediction(Base):
    __tablename__ = "Prediction"

    id: Mapped[BigInteger] = mapped_column(
        BigInteger,
        unique=True,
        index=True,
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )

    profile_id: Mapped[BigInteger] = mapped_column(BigInteger, nullable=False)

    prediction: Mapped[str] = mapped_column(String, nullable=False)

    prediction_type: Mapped[PredictionType] = mapped_column(
        SAEnum(PredictionType), nullable=False
    )

    recognition_str: Mapped[str] = mapped_column(
        String,
        nullable=True, 
    )

    def __doc__(self):
        return f"{__class__.__name__}({self.id})"

    def __str__(self):
        return f"({self.id})"
