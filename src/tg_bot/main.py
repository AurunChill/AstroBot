import asyncio
import pytz

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from bot_ import bot, dispatcher
from handlers import all_routers
from handlers.background.mailing import send_mailing
from middleware import register_middlewares
from logger import bot_logger


async def start_bot():
    bot_logger.info('Bot started')
    register_middlewares(dispatcher)
    dispatcher.include_routers(*all_routers)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(
        bot,
        allowed_updates=[
            'message', 'callback_query'
        ]
    )

async def run_app():
    await asyncio.gather(
        start_bot(),
    )


if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    moscow_timezone = pytz.timezone('Europe/Moscow')
    scheduler.add_job(run_app)
    scheduler.add_job(send_mailing, trigger=CronTrigger(hour=7, minute=0, timezone=moscow_timezone))
    scheduler.start()
    asyncio.get_event_loop().run_forever()