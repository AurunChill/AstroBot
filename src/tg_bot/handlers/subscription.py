from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from logger import bot_logger
from handlers.basic import handle_help_cmd, handle_menu_cmd
from handlers.profile import handle_profile_cmd
from database.user.models import Subscription
from database.user.service import find_user_by_id


subscription_router = Router(name='subscription')

# @subscription_router.message(Command("subscription"))
# async def handle_subscription_cmd(message: Message, state: FSMContext):
#     bot_logger.info(f"User {message.from_user.id} using command /subscription")
#     user_id = message.from_user.id
#     user = await find_user_by_id(user_id=user_id)
#     if user.subscription == Subscription.FOREVER