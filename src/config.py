from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_PASS: str
    DB_USER: str
    OPEN_WEATHER_KEY: str
    SECRET: str
    SECRET_M: str

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()
