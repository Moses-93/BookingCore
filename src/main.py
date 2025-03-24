import os
import sys
import logging
from fastapi import FastAPI
from src.core.dependencies.factories import get_api_factory
from src.core.dependencies.database import register_db_shutdown_event

from src.core import middleware, config

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

app = FastAPI(title="Booking API")

app.add_middleware(middleware.AuthSubscriptionMiddleware)

app.add_middleware(
    middleware.TokenValidationMiddleware, api_token=config.settings.api_token
)
app.include_router(get_api_factory().create_main_router_v1(), prefix="/api/v1")

register_db_shutdown_event(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
