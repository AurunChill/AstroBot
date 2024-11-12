from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from database.predictions.models import Prediction
from logger import db_query_logger as logger


async def create_prediction(
    session: AsyncSession, prediction: Prediction
) -> Prediction:
    """Create a new prediction record."""
    session.add(prediction)
    await session.commit()
    await session.refresh(prediction)
    logger.info(f"Prediction created: {prediction}")
    return prediction


async def delete_prediction(
    session: AsyncSession, prediction_id: int
) -> Optional[Prediction]:
    """Delete a prediction by its ID."""
    prediction = await find_prediction_by_id(session, prediction_id)
    if prediction is None:
        logger.warning(f"Prediction with ID {prediction_id} not found for deletion.")
        return None

    await session.delete(prediction)
    await session.commit()
    logger.info(f"Prediction deleted: {prediction}")
    return prediction


async def find_prediction_by_id(
    session: AsyncSession, prediction_id: int
) -> Optional[Prediction]:
    """Find a prediction by its ID."""
    stmt = select(Prediction).where(Prediction.id == prediction_id)
    result = await session.execute(stmt)
    prediction = result.scalars().first()
    logger.info(f"Prediction fetched by ID {prediction_id}: {prediction}")
    return prediction


async def find_prediction_by_profile_id_and_date(
    session: AsyncSession, profile_id: int, prediction_date: datetime
) -> List[Prediction]:
    """Find predictions by profile ID and prediction date."""
    stmt = select(Prediction).where(
        Prediction.profile_id == profile_id,
        Prediction.prediction_date == prediction_date,
    )
    result = await session.execute(stmt)
    predictions = result.scalars().all()
    logger.info(
        f"Predictions fetched for profile ID {profile_id} and date {prediction_date}: {predictions}"
    )
    return predictions
