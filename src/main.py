import sys
import logging
from fastapi import FastAPI
from api.v1.router import create_main_router
from core import middleware, config


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/logs.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


def main() -> FastAPI:
    """FastAPI application factory."""

    app = FastAPI(title="Booking API")

    app.add_middleware(middleware.AuthSubscriptionMiddleware)

    app.add_middleware(
        middleware.TokenValidationMiddleware, api_token=config.settings.api_token
    )
    app.include_router(create_main_router(), prefix="/api/v1")

    return app


app = main()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
