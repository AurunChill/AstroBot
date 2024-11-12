from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from logger import bot_logger


basic_router = Router(name='basic')


@basic_router.message(Command('start'))
async def handle_start(message: Message) -> Message:
    bot_logger.info(f'User {message.from_user.id} using command /start')
    return await message.answer(text=_('welcome'))


@basic_router.message(Command('help'))
async def handle_help(message: Message) -> Message:
    bot_logger.info(f'User {message.from_user.id} using command /help')
    return await message.answer(text=_('help_message'))