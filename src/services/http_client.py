from httpx import AsyncClient


class HTTPClient:
    def __init__(self, base_url: str = "", timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self.client = None

    async def __aenter__(self):
        self.client = AsyncClient(base_url=self.base_url, timeout=self.timeout)
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
