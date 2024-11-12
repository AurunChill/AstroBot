from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Prediction(Base):
    __tablename__ = 'Prediction'

    id: Mapped[BigInteger] = mapped_column(
        BigInteger, unique=True, index=True, nullable=False, primary_key=True, autoincrement=True
    )
    
    profile_id: Mapped[BigInteger] = mapped_column(
        BigInteger, nullable=False
    )

    prediction_date: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False
    )

    prediction: Mapped[str] = mapped_column(
        String, nullable=False
    )

    def __doc__(self):
        return f'{__class__.__name__}({self.id})'

    def __str__(self):
        return f'({self.id})'