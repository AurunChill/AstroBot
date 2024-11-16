from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from datetime import datetime

from logger import bot_logger
from keyboards.inline.callback import EventsCallback
from keyboards.reply.common import get_menu_reply
from keyboards.inline.events import (
    get_events_inline,
    get_duration_freely_inline,
    get_duration_paid_inline,
)
from gpt.template import load_template, inject_profile_into_template, TemplateType
from gpt.gpt import send_gpt_request
from database.user.models import Subscription
from database.user.service import find_user_by_id
from database.profile.service import find_current_profile_by_user_id
from database.predictions.models import Prediction, PredictionType
from database.predictions.service import (
    create_prediction,
    find_prediction_by_recognition_and_type,
)


event_router = Router(name="event-router")


async def make_event(user_id: int, theme: str, duration: str) -> str:
    data = datetime.today().strftime('%m.%Y') + ' ' + theme + ' ' + duration
    user = await find_user_by_id(user_id=user_id)
    bot_logger.info(user.name)
    user_profile = await find_current_profile_by_user_id(user_id=user_id)

    db_event = await find_prediction_by_recognition_and_type(
        recognition_str=data,
        prediction_type=PredictionType.EVENT
    )

    if db_event:
        return db_event.prediction
    else:
        template = await load_template(locale=user.locale, template_type=TemplateType.EVENT)
        prompt = await inject_profile_into_template(
            extra=f"на {duration} дней, текущая дата (месяц, год) {data.split()[0]}. Тема расчета: {theme}!", template=template, profile=user_profile
        )
        response = await send_gpt_request(prompt=prompt)

        await create_prediction(Prediction(
            profile_id = user_profile.id,
            prediction = response,
            prediction_type = PredictionType.EVENT,
            recognition_str = data
        ))

        return response


@event_router.message(Command("events"))
async def handle_event_cmd(message: Message, state: FSMContext):
    bot_logger.info(f"User {message.from_user.id} using command /events")
    await message.answer(
        text=_("wanna_date_msg"), reply_markup=await get_events_inline()
    )


async def handle_event_theme(callback: CallbackQuery, theme: str):
    user_id = callback.message.chat.id
    user = await find_user_by_id(user_id=user_id)
    if user.subscription is Subscription.FREELY:
        await callback.message.answer(
            text=_("choose_duration_msg"),
            reply_markup=await get_duration_freely_inline(theme=theme),
        )
    else:
        await callback.message.answer(
            text=_("choose_duration_msg"),
            reply_markup=await get_duration_paid_inline(theme=theme),
        )


@event_router.callback_query(F.data.startswith(EventsCallback.STUDY))
async def handle_study_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    await handle_event_theme(callback=callback, theme="study")
    await callback.answer()


@event_router.callback_query(F.data.startswith(EventsCallback.MOOD))
async def handle_mood_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    await handle_event_theme(callback=callback, theme="mood")
    await callback.answer()


@event_router.callback_query(F.data.startswith(EventsCallback.LOVE))
async def handle_love_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    await handle_event_theme(callback=callback, theme="love")
    await callback.answer()


@event_router.callback_query(F.data.startswith(EventsCallback.INCOME))
async def handle_income_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    await handle_event_theme(callback=callback, theme="income")
    await callback.answer()


@event_router.callback_query(F.data.startswith(EventsCallback.SUCCESS))
async def handle_success_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    await handle_event_theme(callback=callback, theme="success")
    await callback.answer()


@event_router.callback_query(F.data.startswith(EventsCallback.DURATION_45))
async def handle_duration_45_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    data = callback.data.split()
    theme = data[1]
    user_id = callback.message.chat.id
    event = await make_event(user_id=user_id,theme=theme, duration="45")
    await callback.message.answer(text=event, reply_markup=await get_menu_reply())
    await callback.answer()


@event_router.callback_query(F.data.startswith(EventsCallback.DURATION_90))
async def handle_duration_90_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    data = callback.data.split()
    theme = data[1]
    user_id = callback.message.chat.id
    event = await make_event(user_id=user_id, theme=theme, duration="90")
    await callback.message.answer(text=event, reply_markup=await get_menu_reply())    
    await callback.answer()


@event_router.callback_query(F.data.startswith(EventsCallback.DURATION_180))
async def handle_duration_180_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    data = callback.data.split()
    theme = data[1]
    user_id = callback.message.chat.id
    event = await make_event(user_id=user_id, theme=theme, duration="180")
    await callback.message.answer(text=event, reply_markup=await get_menu_reply())
    await callback.answer()


@event_router.callback_query(F.data.startswith(EventsCallback.DURATION_365))
async def handle_duration_365_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    data = callback.data.split()
    theme = data[1]
    user_id = callback.message.chat.id
    event = await make_event(user_id=user_id, theme=theme, duration="365")
    await callback.message.answer(text=event, reply_markup=await get_menu_reply())
    await callback.answer()