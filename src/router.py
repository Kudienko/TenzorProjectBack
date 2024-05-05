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

import json


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
async def get_similar_cities(city_query: str):
    cities_str = await cache_backend.get("cities")
    cities = json.loads(cities_str) if cities_str else []
    search_results = [city for city in cities if city_query.lower() in city["city_name"].lower()]
    return search_results


# Загрузка redis и городов при старте сервера
@router.on_event("startup")
async def load_cities():
    global cache_backend
    redis = aioredis.from_url("redis://localhost")
    cache_backend = RedisBackend(redis)
    FastAPICache.init(cache_backend, prefix="fastapi-cache")
    with open('cities.json', 'r', encoding='utf-8-sig') as f:
        city_data = json.load(f)
        cities = city_data if isinstance(city_data, list) else city_data.get("city", [])
        await cache_backend.set("cities", json.dumps(cities))
