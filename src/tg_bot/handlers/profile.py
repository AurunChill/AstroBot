from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from logger import bot_logger
from config import settings
from filters.access import ProfileRegistered
from states.profile import RegistrationStates
from database.profile.models import Profile
from database.profile.service import (
    find_profiles_by_user_id,
    delete_profile,
    create_profile,
)
from keyboards.inline.profile import profile_action_keyboard, profile_inline_keyboard
from keyboards.inline.callback import ProfileCallback


profile_router = Router(name="profile")


