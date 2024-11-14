from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback import ProfileCallback
from database.profile.models import Profile

async def profile_inline_keyboard(profiles: list[Profile]):
    buttons = []
    for profile in profiles:
        buttons.append([
            InlineKeyboardButton(text=profile.title, callback_data=ProfileCallback.PROFILE + str(profile.id))
        ])
    buttons.append([
        InlineKeyboardButton(text=_("register"), callback_data=ProfileCallback.REGISTER)
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def profile_action_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("change_profile"), callback_data=ProfileCallback.CHANGE_PROFILE)],
            [InlineKeyboardButton(text=_("edit_data"), callback_data=ProfileCallback.EDIT_DATA)],
            [InlineKeyboardButton(text=_("delete_profile"), callback_data=ProfileCallback.DELETE_PROFILE)],
        ]
    )
