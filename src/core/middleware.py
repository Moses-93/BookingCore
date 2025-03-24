import logging
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import datetime

from db.models.subscription import Subscription
from db.models.user import User
from services.notifications import notification_service
from .dependencies import get_db, verify_user


logger = logging.getLogger(__name__)


class TokenValidationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, api_token: str):
        super().__init__(app)
        self.api_token = api_token

    async def dispatch(self, request: Request, call_next):
        logger.info(f"path: {request.url.path}")
        if request.url.path in [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/api/v1/payments/callback/",
            "https://10b9-185-70-17-81.ngrok-free.app/api/v1/payments/callback/",
        ]:
            return await call_next(request)
        logger.info(f"Перевірка токену для запиту {request.url}")

        token = request.headers.get("Authorization")
        if not token or token != f"Bearer {self.api_token}":
            logger.warning("Невірний токен")
            raise HTTPException(status_code=401, detail="Invalid token")
        logger.info("Токен успішно підтверджений")

        response = await call_next(request)
        return response


class AuthSubscriptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"path: {request.url.path}")
        if (
            request.url.path
            in [
                "/api/v1/users",
                "/api/v1/users/",
                "/api/v1/payments/callback/",
                "https://10b9-185-70-17-81.ngrok-free.app/api/v1/payments/callback/",
            ]
            and request.method == "POST"
        ):
            return await call_next(request)
        logger.info("Перевірка підписки користувача!")
        async for db in get_db():
            user: User = await verify_user(request, db)
            if not user:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "User not found"},
                )
            logger.info(f"User:{user}")

            request.state.user = user

            if user.role == "master" and user.subscription:
                subscription: Subscription = user.subscription

                grace_period = subscription.end_date + datetime.timedelta(days=10)
                if datetime.datetime.now() > grace_period and user.is_active:
                    logger.warning(
                        f"Майстер {user.name} | {user.chat_id} повністю деактивований"
                    )
                    user.is_active = False
                    await db.commit()

                    msg = (
                        f"{user.name}, на жаль, вимушені деактивувати ваш профіль через неоплату підписки.\n"
                        "Тепер ви не зможете приймати записи від клієнтів!"
                    )
                    await notification_service.send_message(user.chat_id, msg)

        response = await call_next(request)
        return response
