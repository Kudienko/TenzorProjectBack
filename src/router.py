from fastapi import APIRouter, Depends, HTTPException
from src.config import settings
from src.http_client import OpenWeatherHTTPClient
# from async_lru import alru_cache

from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.database import CustomUser
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate, UserUpdate

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis


router = APIRouter(
    prefix="/api"
)

fastapi_users = FastAPIUsers[CustomUser, int](
    get_user_manager,
    [auth_backend],
)

cache_backend = None

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@router.get("/hello")
def hello():
    return {"message": "Hello!"}


@router.get("/get_weather")
@cache(expire=120)
async def get_weather(lat: str, lon: str):
    open_weather_client = OpenWeatherHTTPClient(base_url="https://api.openweathermap.org",
                                                api_key=settings.OPEN_WEATHER_KEY)
    return await open_weather_client.get_weather(lat=lat, lon=lon)


@router.get("/get_city")
@cache(expire=120)
async def get_similar_cities(city: str):
    open_weather_client = OpenWeatherHTTPClient(base_url="https://api.openweathermap.org",
                                                api_key=settings.OPEN_WEATHER_KEY)
    return await open_weather_client.get_city_info(city=city)


# Загрузка redis при старте сервера
@router.on_event("startup")
async def load_cities():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
