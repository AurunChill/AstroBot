from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

import re
from datetime import datetime

from logger import bot_logger
from handlers.register import handle_register_cmd
from filters.access import ProfileRegistered
from states.profile import ChangeDataStates
from keyboards.reply.profile import get_location_reply
from keyboards.reply.common import get_menu_reply
from keyboards.inline.callback import ProfileCallback
from keyboards.inline.profile import (
    get_profile_inline,
    get_profile_list_inline,
    get_change_profile_data_inline,
)
from database.user.service import find_user_by_id, update_user
from database.profile.service import (
    find_current_profile_by_user_id,
    find_profiles_by_user_id,
    find_profile_by_id,
    delete_profile,
    update_profile,
)
from keyboards.reply.common import get_decline_reply


profile_router = Router(name="profile")


@profile_router.message(Command("profile"), ProfileRegistered())
async def handle_profile_cmd(message: Message, state: FSMContext):
    bot_logger.info(f"User {message.from_user.id} using command /profile")
    user_id = message.from_user.id
    profile = await find_current_profile_by_user_id(user_id=user_id)
    await message.answer(str(profile), reply_markup=await get_profile_inline())


@profile_router.callback_query(F.data.startswith(ProfileCallback.CHANGE_PROFILE))
async def handle_change_profile_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    user_id = callback.message.chat.id
    user_profiles = await find_profiles_by_user_id(user_id=user_id)
    await callback.message.answer(
        text=_("choose_profile_msg"),
        reply_markup=await get_profile_list_inline(profiles=user_profiles),
    )
    await callback.answer()


@profile_router.callback_query(F.data.startswith(ProfileCallback.CHANGE_DATA))
async def handle_change_data_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    await callback.message.answer(
        text=_("prefer_to_change_msg"),
        reply_markup=await get_change_profile_data_inline(),
    )
    await callback.answer()


@profile_router.callback_query(F.data.startswith(ProfileCallback.DELETE_PROFILE))
async def handle_delete_profile_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    user_id = callback.message.chat.id
    user = await find_user_by_id(user_id=user_id)
    profile = await find_profile_by_id(profile_id=user.current_profile_id)
    await delete_profile(profile_id=profile.id)
    user_profiles = await find_profiles_by_user_id(user_id=user_id)
    if user_profiles and len(user_profiles) > 0:
        new_current_profile = user_profiles[0]
        user.current_profile_id = new_current_profile.id
        await update_user(user_id=user_id, updated_user=user)
        await callback.message.answer(text=_("profile_deleted_changed_msg"))
    else:
        await callback.message.answer(text=_("profile_deleted_new_msg"))
    await callback.answer()


@profile_router.callback_query(F.data.startswith(ProfileCallback.CHANGE_STATUS))
async def handle_change_status_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    await callback.answer()


@profile_router.callback_query(F.data.startswith(ProfileCallback.PROFILE_OPTION))
async def handle_profile_option_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    data = callback.data.split()
    profile_id = int(data[1])
    user_id = callback.message.chat.id
    user = await find_user_by_id(user_id=user_id)
    user.current_profile_id = profile_id
    await update_user(user_id=user_id, updated_user=user)
    await callback.message.answer(text=_("profile_changed_msg"))
    await callback.answer()


@profile_router.callback_query(F.data.startswith(ProfileCallback.ADD_PROFILE))
async def handle_add_profile_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    await handle_register_cmd(message=callback.message, state=state)
    await callback.answer()


@profile_router.callback_query(F.data.startswith(ProfileCallback.CHANGE_TITLE))
async def handle_change_title_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    await state.set_state(ChangeDataStates.title.state)
    await callback.message.answer(
        text=_("send_prof_name_msg"), reply_markup=await get_decline_reply()
    )
    await callback.answer()


@profile_router.callback_query(F.data.startswith(ProfileCallback.CHANGE_BIRTH_DATE))
async def handle_change_birth_date_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    await state.set_state(ChangeDataStates.birth_date.state)
    await callback.message.answer(
        text=_("send_birth_date_msg"), reply_markup=await get_decline_reply()
    )
    await callback.answer()


@profile_router.callback_query(F.data.startswith(ProfileCallback.CHANGE_BIRTH_TIME))
async def handle_change_birth_time_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    await state.set_state(ChangeDataStates.birth_time.state)
    await callback.message.answer(
        text=_("send_birth_time_msg"), reply_markup=await get_decline_reply()
    )
    await callback.answer()


@profile_router.callback_query(F.data.startswith(ProfileCallback.CHANGE_BIRTH_LOCATION))
async def handle_change_birth_location_callback(
    callback: CallbackQuery, state: FSMContext
):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    await state.set_state(ChangeDataStates.birth_location.state)
    await callback.message.answer(
        text=_("send_birth_location_msg"), reply_markup=await get_decline_reply()
    )
    await callback.answer()


@profile_router.callback_query(F.data.startswith(ProfileCallback.CHANGE_LOCATION))
async def handle_change_location_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f"User {callback.from_user.id} using callback {callback.data}")
    await state.set_state(ChangeDataStates.current_location.state)
    await callback.message.answer(
        text=_("send_current_location_msg"), reply_markup=await get_location_reply()
    )
    await callback.answer()


@profile_router.message(ChangeDataStates.title)
async def handle_profile_change_title(message: Message, state: FSMContext):
    bot_logger.info(f"User {message.from_user.id} sending title: {message.text}")
    title = message.text
    if title:
        user_id = message.from_user.id
        current_profile = await find_current_profile_by_user_id(user_id=user_id)
        current_profile.title = title
        await update_profile(
            profile_id=current_profile.id, updated_profile=current_profile
        )
        await message.answer(
            text=_("title_changed_msg"), reply_markup=await get_menu_reply()
        )
        await state.clear()
    else:
        await message.answer(text=_("prof_name_err_msg"))


@profile_router.message(ChangeDataStates.birth_date)
async def handle_profile_change_birth_date(message: Message, state: FSMContext):
    bot_logger.info(f"User {message.from_user.id} sending birth date: {message.text}")
    date_pattern = r"^\d{2}\.\d{2}\.\d{4}$"
    if message.text and re.match(date_pattern, message.text):
        user_id = message.from_user.id
        current_profile = await find_current_profile_by_user_id(user_id=user_id)
        try:
            current_profile.birth_date = datetime.strptime(
                message.text, "%d.%m.%Y"
            ).date()
            await update_profile(
                profile_id=current_profile.id, updated_profile=current_profile
            )
            await message.answer(
                text=_("birth_date_changed_msg"), reply_markup=await get_menu_reply()
            )
        except ValueError:
            await message.answer(text=_("birth_date_err_msg"))
        finally:
            await state.clear()
    else:
        await message.answer(text=_("birth_date_err_msg"))


@profile_router.message(ChangeDataStates.birth_time)
async def handle_profile_change_birth_time(message: Message, state: FSMContext):
    bot_logger.info(f"User {message.from_user.id} sending birth time: {message.text}")
    time_pattern = r"^\d{2}:\d{2}$"
    if message.text and re.match(time_pattern, message.text):
        user_id = message.from_user.id
        current_profile = await find_current_profile_by_user_id(user_id=user_id)
        try:
            current_profile.birth_time = datetime.strptime(message.text, "%H:%M").time()
            await update_profile(
                profile_id=current_profile.id, updated_profile=current_profile
            )
            await message.answer(
                text=_("birth_time_changed_msg"), reply_markup=await get_menu_reply()
            )
        except ValueError:
            await message.answer(text=_("birth_time_err_msg"))
        finally:
            await state.clear()
    else:
        await message.answer(text=_("birth_time_err_msg"))


@profile_router.message(ChangeDataStates.birth_location)
async def handle_profile_change_birth_location(message: Message, state: FSMContext):
    bot_logger.info(f"User {message.from_user.id} sending birth location.")
    if message.location:
        user_id = message.from_user.id
        current_profile = await find_current_profile_by_user_id(user_id=user_id)
        current_profile.birth_longitude = float(message.location.longitude)
        current_profile.birth_latitude = float(message.location.latitude)
        await update_profile(
            profile_id=current_profile.id, updated_profile=current_profile
        )
        await message.answer(
            text=_("birth_location_changed_msg"), reply_markup=await get_menu_reply()
        )
        await state.clear()
    else:
        await message.answer(text=_("birth_location_err_msg"))


@profile_router.message(ChangeDataStates.current_location)
async def handle_profile_change_current_location(message: Message, state: FSMContext):
    bot_logger.info(f"User {message.from_user.id} sending current location.")
    if message.location:
        user_id = message.from_user.id
        current_profile = await find_current_profile_by_user_id(user_id=user_id)
        current_profile.location_longitude = float(message.location.longitude)
        current_profile.location_latitude = float(message.location.latitude)
        await update_profile(
            profile_id=current_profile.id, updated_profile=current_profile
        )
        await message.answer(
            text=_("current_location_changed_msg"), reply_markup=await get_menu_reply()
        )
        await state.clear()
    else:
        await message.answer(text=_("current_location_err_msg"))
