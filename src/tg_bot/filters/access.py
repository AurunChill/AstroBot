from aiogram.types import Message
from aiogram.filters import BaseFilter
from aiogram.utils.i18n import gettext as _

from database.profile.service import find_profiles_by_user_id


class ProfileRegistered(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        profiles = find_profiles_by_user_id(user_id)
        if profiles and len(profiles) > 0:
            return True
        await message.answer(text=_('not_registered'))
        return False