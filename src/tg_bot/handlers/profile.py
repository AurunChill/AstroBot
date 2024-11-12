from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from logger import bot_logger
from config import settings
from filters.access import ProfileRegistered


profile_router = Router(name='profile')


@profile_router(Command('profile'), ProfileRegistered())
async def handle_profile_cmd(message: Message, state: FSMContext):
    bot_logger.info(f'User {message.from_user.id} using command /profile')



@profile_router(Command('change_profile'), ProfileRegistered())
async def handle_change_profile_cmd(message: Message, state: FSMContext):
    bot_logger.info(f'User {message.from_user.id} using command /change_profile')
  
# Commands:
# /profile - Show user profile
# /change_profile - Change user profile

