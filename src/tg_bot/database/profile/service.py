from sqlalchemy import select, update
from typing import List, Optional

from database.profile.models import Profile
from logger import db_query_logger as logger
from database.db import session_maker


async def create_profile(profile: Profile) -> Profile:
    """Create a new profile record."""
    async with session_maker() as session:
        session.add(profile)
        await session.commit()
        await session.refresh(profile)
        logger.info(f'Profile created: {profile}')
        return profile


async def find_profile_by_id(profile_id: int) -> Optional[Profile]:
    """Find a profile by its ID."""
    async with session_maker() as session:
        stmt = select(Profile).where(Profile.id == profile_id)
        result = await session.execute(stmt)
        profile = result.scalars().first()
        logger.info(f'Profile fetched by ID {profile_id}: {profile}')
        return profile


async def find_profiles_by_user_id(user_id: int) -> List[Profile]:
    """Find all profiles associated with a user ID."""
    async with session_maker() as session:
        stmt = select(Profile).where(Profile.user_id == user_id)
        result = await session.execute(stmt)
        profiles = result.scalars().all()
        logger.info(f'Profiles fetched for user ID {user_id}: {profiles}')
        return profiles


async def update_profile(profile_id: int, updated_data: Profile) -> Optional[Profile]:
    """Update a profile's data."""
    async with session_maker() as session:
        stmt = update(Profile).where(Profile.id == profile_id).values(
            user_name=updated_data.user_name,
            title=updated_data.title,
            birth_date=updated_data.birth_date,
            birth_time=updated_data.birth_time,
            birth_timezone=updated_data.birth_timezone,
            birth_latitude=updated_data.birth_latitude,
            birth_longitude=updated_data.birth_longitude,
            location_latitude=updated_data.location_latitude,
            location_longitude=updated_data.location_longitude,
        )
        await session.execute(stmt)
        await session.commit()

        updated_profile = await find_profile_by_id(profile_id)
        logger.info(f'Profile updated: {updated_profile}')
        return updated_profile


async def delete_profile(profile_id: int) -> Optional[Profile]:
    """Delete a profile by its ID."""
    async with session_maker() as session:
        profile = await find_profile_by_id(profile_id)
        if profile is None:
            logger.warning(f'Profile with ID {profile_id} not found for deletion.')
            return None

        await session.delete(profile)
        await session.commit()
        logger.info(f'Profile deleted: {profile}')
        return profile