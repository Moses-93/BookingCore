import logging
from typing import Any
from fastapi import HTTPException


logger = logging.getLogger(__name__)


def ensure_resource_exists(
    data: Any, status_code: int = 404, message: str = "Resource not found"
):
    if not data:
        raise HTTPException(status_code=status_code, detail=message)
    return data
