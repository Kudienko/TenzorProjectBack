from aiohttp import ClientSession
# from async_lru import alru_cache
from fastapi_cache.decorator import cache
from fastapi import HTTPException


class HTTPClient:
    def __init__(self, base_url: str, api_key: str):
        self._session = ClientSession(
            base_url=base_url
        )
        self._api_key = api_key


class OpenWeatherHTTPClient(HTTPClient):
    @cache(expire=120)
    async def get_weather(self, lat: str, lon: str):
        try:
            async with self._session.get(
                    f'/data/2.5/forecast?lat={lat}&lon={lon}&appid={self._api_key}&lang=ru&units=metric') as response:
                result = await response.json()
                return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Произошла ошибка при получении погоды. {e.message}")
        finally:
            await self._session.close()

    @cache(expire=120)
    async def get_city_info(self, city: str):
        try:
            async with self._session.get(
                    f'/geo/1.0/direct?q={city}&limit=4&appid={self._api_key}') as response:
                result = await response.json()
                return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Произошла ошибка при получении города. {e.message}")
        finally:
            await self._session.close()
