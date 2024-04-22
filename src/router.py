from fastapi import APIRouter
from src.config import settings
from src.http_client import OpenWeatherHTTPClient

router = APIRouter(
    prefix="/api"
)


@router.get("/hello")
def hello():
    return {"message": "Hello!"}


@router.get("/get_weather/{city}")
async def get_weather(city: str):
    open_weather_client = OpenWeatherHTTPClient(base_url="https://api.openweathermap.org", city=city,
                                                api_key=settings.OPEN_WEATHER_KEY)
    return await open_weather_client.get_weather()
