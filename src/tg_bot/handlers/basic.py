from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from logger import bot_logger
from keyboards.reply.common import get_menu_reply
from keyboards.inline.basic import get_language_inline
from keyboards.inline.callback import BasicCallback
from database.user.models import User
from database.user.service import find_user_by_id, create_user, update_user

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
    await message.answer(text=_('start_msg'), reply_markup=await get_menu_reply())
    await handle_lang_cmd(message=message, state=state)


@basic_router.message(Command('help'))
async def handle_help_cmd(message: Message, state: FSMContext):
    bot_logger.info(f'User {message.from_user.id} using command /help')
    await message.answer(text=_('help_msg'))


@basic_router.message(Command('menu'))
async def handle_menu_cmd(message: Message, state: FSMContext):
    bot_logger.info(f'User {message.from_user.id} using command /menu')
    await state.clear()
    await message.answer(text=_('menu_msg'), reply_markup=await get_menu_reply())
    

@basic_router.message(Command('lang'))
async def handle_lang_cmd(message: Message, state: FSMContext):
    bot_logger.info(f'User {message.from_user.id} using command /lang')
    await message.answer(text=_('lang_msg'), reply_markup=await get_language_inline())


@basic_router.callback_query(F.data.startswith(BasicCallback.LANGUAGE))
async def handle_language_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f'User {callback.from_user.id} using callback {callback.data}')
    data = callback.data.split()
    language = data[1]
    user_id = callback.message.chat.id
    user = await find_user_by_id(user_id=user_id)
    user.locale = language
    await update_user(user_id=user_id, updated_user=user)
    await callback.message.edit_text(text=_('lang_msg', locale=language), reply_markup=await get_language_inline())
    await callback.answer()