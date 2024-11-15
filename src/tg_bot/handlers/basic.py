from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from logger import bot_logger
from keyboards.reply.common import get_menu_reply
from database.user.models import User
from database.user.service import find_user_by_id, create_user

basic_router = Router(name='basic')


async def create_user_if_not_exists(user_id: int, user_name: str):
    db_user = await find_user_by_id(user_id=user_id)
    if not db_user:
        await create_user(user=User(id=user_id, name=user_name, locale='ru'))
        bot_logger.info(f'User {user_id} created')


@basic_router.message(Command('start'))
async def handle_start_cmd(message: Message, state: FSMContext):
    bot_logger.info(f'User {message.from_user.id} using command /start')
    user = message.from_user
    await create_user_if_not_exists(user_id=user.id, user_name=user.full_name)
    await message.answer(text=_('start_msg'))


@basic_router.message(Command('help'))
async def handle_help_cmd(message: Message, state: FSMContext):
    bot_logger.info(f'User {message.from_user.id} using command /help')
    await message.answer(text=_('help_msg'))


@basic_router.message(Command('menu'))
async def handle_menu_cmd(message: Message, state: FSMContext):
    bot_logger.info(f'User {message.from_user.id} using command /menu')
    await state.clear()
    await message.answer(text=_('menu_msg'), reply_markup=await get_menu_reply())
    