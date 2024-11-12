from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


PROJECT_PATH = Path(__file__).parent.parent.parent
TG_BOT_FOLDER = PROJECT_PATH / 'src' / 'tg_bot'
ENV_PATH = PROJECT_PATH / '.env'

if not ENV_PATH.exists():
    raise FileNotFoundError(f'{ENV_PATH} does not exist. Please create the .env file with the required variables.')

load_dotenv(dotenv_path=ENV_PATH)
 

class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(ENV_PATH), env_file_encoding='utf-8', extra='allow')


class BotSettings(EnvSettings):
    BOT_TOKEN: str
    ADMIN_IDS: list[int]


class LoggingSettings:
    LOG_PATH = PROJECT_PATH / 'logs'


class GPTSettings(EnvSettings):
    OPENAI_API_KEY: str

    @property
    def GPT_MODEL():
        return 'gpt-4o-mini'

    @property
    def BASE_URL():
        return 'https://api.proxyapi.ru/openai/v1'
    
    @property
    def GPT_TEMPLATES_PATH():
        return TG_BOT_FOLDER / 'gpt' / 'templates'
    

class DatabaseSettings(EnvSettings):
    DB_TYPE: str
    DB_USER: str
    DB_PORT: str
    DB_PASS: str
    DB_HOST: str
    DB_NAME: str

    @property
    def SQLITE_PATH(self):
        return PROJECT_PATH / 'src' / 'tg_bot' / 'database' /'tg_bot.db'
    
    @property
    def DATABASE_URL(self):
        if self.DB_TYPE == 'sqlite':
            return f'sqlite:///{self.SQLITE_PATH}'
        else:
            return f'postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


class LocalesSettings:
    DEFAULT_LOCALE = 'ru'
    I18N_DOMAIN = 'messages'
    LOCALE_PATH = TG_BOT_FOLDER / 'locales'


class Settings:
    bot = BotSettings()
    log = LoggingSettings()
    database = DatabaseSettings()
    locales = LocalesSettings()
    gpt = GPTSettings()


settings = Settings()
