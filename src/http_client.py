from aiohttp import ClientSession


class HTTPClient:
    def __init__(self, base_url: str, city: str, api_key: str):
        self._session = ClientSession(
            base_url=base_url
        )
        self._city = city
        self._api_key = api_key


class OpenWeatherHTTPClient(HTTPClient):
    async def get_weather(self):
        try:
            async with self._session.get(
                    f'/data/2.5/forecast?q={self._city}&appid={self._api_key}&lang=ru&units=metric') as response:
                result = await response.json()
                return result
        finally:
            await self._session.close()