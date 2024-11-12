from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


async def get_test_keyboard() -> ReplyKeyboardMarkup:
    keyboard_buttons = [
        [KeyboardButton(text=_("msgid"), request_contact=True)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True, one_time_keyboard=True)
