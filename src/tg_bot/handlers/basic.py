from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from logger import bot_logger
from keyboards.reply.basic import get_menu_reply


basic_router = Router(name='basic')


@basic_router.message(Command('start'))
async def handle_start_cmd(message: Message, state: FSMContext):
    bot_logger.info(f'User {message.from_user.id} using command /start')
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


@basic_router.message()
async def handle_any_msg(message: Message, state: FSMContext):
    bot_logger.info(f'User {message.from_user.id} sending message: {message.text}')
    await handle_menu_cmd(message=message, state=state)