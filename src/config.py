from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_PASS: str
    DB_USER: str
    OPEN_WEATHER_KEY: str

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()
