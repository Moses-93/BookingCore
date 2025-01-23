import logging
from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger(__name__)


class TokenValidationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, api_token: str):
        super().__init__(app)
        self.api_token = api_token

    async def dispatch(self, request: Request, call_next):
        logger.info(f"Перевірка токену для запиту {request.url}")
        if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
        token = request.headers.get("Authorization")
        if not token or token != f"Bearer {self.api_token}":
            logger.warning("Невірний токен")
            raise HTTPException(status_code=401, detail="Invalid token")
        logger.info("Токен успішно підтверджений")

        response = await call_next(request)
        return response
