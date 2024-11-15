from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

import re
from datetime import datetime

from logger import bot_logger
from states.horoscope import DateState
from keyboards.reply.common import get_decline_reply
from keyboards.inline.callback import HoroscopeCallback
from keyboards.reply.common import get_menu_reply
from keyboards.inline.horoscope import get_horo_inline
from gpt.template import load_template, inject_profile_into_template, TemplateType
from gpt.gpt import send_gpt_request
from database.user.service import find_user_by_id
from database.profile.service import find_current_profile_by_user_id
from database.predictions.models import Prediction, PredictionType
from database.predictions.service import create_prediction, find_prediction_by_recognition_and_type


horoscope_router = Router(name="horoscope")


async def make_horoscope(user_id: int, date: str):
    match date:
        case 'today':
            recognition_str = datetime.today().strftime('%d.%m.%Y')
        case 'month':
            recognition_str = datetime.today().strftime('%m.%Y')
        case _:
            recognition_str = date

    user = await find_user_by_id(user_id=user_id)
    bot_logger.info(user.name)
    user_profile = await find_current_profile_by_user_id(user_id=user_id)

    db_horoscope = await find_prediction_by_recognition_and_type(
        recognition_str=recognition_str,
        prediction_type=PredictionType.HOROSCOPE
    )

    if db_horoscope:
        return db_horoscope.prediction
    else:
        template = await load_template(locale=user.locale, template_type=TemplateType.HOROSCOPE)
        prompt = await inject_profile_into_template(
            date=date, template=template, profile=user_profile
        )
        response = await send_gpt_request(prompt=prompt)

        await create_prediction(Prediction(
            profile_id = user_profile.id,
            prediction = response,
            prediction_type = PredictionType.HOROSCOPE,
            recognition_str = recognition_str
        ))

        return response


@horoscope_router.message(Command("horoscope"))
async def handle_horoscope_cmd(message: Message, state: FSMContext):
    bot_logger.info(f"User {message.from_user.id} using command /horoscope")
    await message.answer(
        text=_("create_horoscope_option_msg"), reply_markup=await get_horo_inline()
    )


@horoscope_router.callback_query(F.data.startswith(HoroscopeCallback.TODAY))
async def handle_today_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    horoscope = await make_horoscope(user_id=callback.message.chat.id, date="today")
    await callback.message.answer(text=horoscope)
    await callback.answer()


@horoscope_router.callback_query(F.data.startswith(HoroscopeCallback.MONTH))
async def handle_month_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    horoscope = await make_horoscope(user_id=callback.message.chat.id, date="month")
    await callback.message.answer(text=horoscope)
    await callback.answer()


@horoscope_router.callback_query(F.data.startswith(HoroscopeCallback.DATE))
async def handle_date_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    await callback.message.answer(
        text=_("ask_date_msg"), reply_markup=await get_decline_reply()
    )
    await state.set_state(DateState.date.state)
    await callback.answer()


@horoscope_router.message(DateState.date)
async def handle_date(message: Message, state: FSMContext):
    bot_logger.info(f"User {message.from_user.id} sending date: {message.text}")
    date_pattern = r"^\d{2}.\d{2}.\d{4}$"
    if message.text and re.match(date_pattern, message.text):
        date = message.text
        horoscope = await make_horoscope(user_id=message.from_user.id, date=date)
        await message.answer(text=horoscope, reply_markup=await get_menu_reply())
        await state.clear()
    else:
        await message.answer(text=_("date_error_msg"))
