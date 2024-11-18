from aiogram.utils.i18n import gettext as _
from yandex_geocoder import Client

from config import settings
from logger import bot_logger

client = Client(settings.location.DECODER_API_KEY)


async def get_location(locale: str, latitude: float, longitude: float) -> str:
    try:
        bot_logger.info(f"Getting location for {latitude}, {longitude}")
        address = client.address(latitude, longitude)
        bot_logger.info(f"Got location: {address}")
        return address
    except Exception as e:
        bot_logger.error(e)
        return _("location_error_msg")


# async def get_location(locale: str, latitude: float, longitude: float) -> str:
#     """Fetch location description using latitude and longitude."""
#     try:
#         geolocator = Nominatim(user_agent="geoapiExercises")
#         location = geolocator.reverse((latitude, longitude), language=locale)
        
#         if location:
#             address = location.raw['address']
#             city = address.get('city', '') or address.get('town', '') or address.get('village', '')
#             country = address.get('country', '')
            
#             return f"{city}, {country}" if city and country else _('location_not_found_msg')
#         else:
#             return _('location_not_found_msg')
#     except Exception as e:
#         bot_logger.error(e)
#         return _('location_error_msg')