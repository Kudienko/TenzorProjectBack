from fastapi import APIRouter, Depends, HTTPException
from src.config import settings
from src.http_client import OpenWeatherHTTPClient
from async_lru import alru_cache

from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.database import CustomUser
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate, UserUpdate

router = APIRouter(
    prefix="/api"
)

fastapi_users = FastAPIUsers[CustomUser, int](
    get_user_manager,
    [auth_backend],
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
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


@router.get("/get_weather/{city}")
@alru_cache
async def get_weather(city: str):
    open_weather_client = OpenWeatherHTTPClient(base_url="https://api.openweathermap.org", city=city,
                                                api_key=settings.OPEN_WEATHER_KEY)
    return await open_weather_client.get_weather()
