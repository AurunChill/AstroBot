from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton


# Callback data
TEST_1 = "test1"
TEST_2 = "test2"


async def test_inline_keyboard() -> InlineKeyboardMarkup:
    button_list = [
        [
            InlineKeyboardButton(text=_("msgid"), callback_data=TEST_1),
            InlineKeyboardButton(text=_("msgid"), callback_data=TEST_2),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=button_list)    
