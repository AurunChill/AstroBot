import re

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from logger import bot_logger
from config import settings
from states.test import TestStates
from keyboards.inline.survey import (
    test_inline_keyboard,
    TEST_1,
    TEST_2,
)
from keyboards.reply.test import get_test_keyboard


test_router = Router(name='survey')


@test_router.message(Command('register'))
async def handle_register(message: Message) -> Message:
    # Command example
    bot_logger.info(f'User {message.from_user.id} using command /register')
    return await message.answer(
        text=_('register'), reply_markup=await test_inline_keyboard()
    )


@test_router.callback_query(F.data.startswith(TEST_1))
async def handle_doc_image_opt(
    callback: CallbackQuery, state: FSMContext
) -> MediaGroupBuilder:
    # Callback example
    bot_logger.info(f'User {callback.from_user.id} using callback {callback.data}')
    await state.set_state(TestStates.test1.state)
    await callback.answer()


@test_router.message(TestStates.test1)
async def process_phone_number(message: Message, state: FSMContext) -> Message:
    # FSM example
    bot_logger.info(f'User {message.from_user.id} sending phone number: {message.text}')
    state.clear()
        