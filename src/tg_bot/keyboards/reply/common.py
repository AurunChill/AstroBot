from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


async def get_menu_reply() -> ReplyKeyboardMarkup:
    keyboard_buttons = [
        [KeyboardButton(text=_('horoscope_btn')), KeyboardButton(text=_('event_btn'))],
        [KeyboardButton(text=_('profile_btn')), KeyboardButton(text=_('help_btn'))],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True)


async def get_decline_reply() -> ReplyKeyboardMarkup:
    keyboard_buttons = [[KeyboardButton(text=_('decline_btn'))]]
    return ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True, one_time_keyboard=True)