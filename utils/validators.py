import logging
from typing import Any, Dict
from fastapi import HTTPException
from db.models.user import User


logger = logging.getLogger(__name__)


def ensure_resource_exists(
    data, status_code: int = 404, message: str = "Resource not found"
):
    if not data:
        raise HTTPException(status_code=status_code, detail=message)
    return data
