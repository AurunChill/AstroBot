from typing import Any

from aiogram.types import TelegramObject
from aiogram.utils.i18n.middleware import I18nMiddleware

from config import settings


class LocaleMiddleware(I18nMiddleware):
    DEFAULT_LANGUAGE_CODE = settings.locales.DEFAULT_LOCALE

    async def get_locale(self, event: TelegramObject, data: dict[str, Any]) -> str:
        return self.DEFAULT_LANGUAGE_CODE