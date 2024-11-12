from aiogram.filters import BaseFilter
from aiogram.types import Message

from database.profile.service import find_profiles_by_user_id


class ProfileRegistered(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        profiles = find_profiles_by_user_id(user_id)
        return profiles is not None