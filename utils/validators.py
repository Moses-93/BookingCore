from typing import Any, Dict
from fastapi import HTTPException
from db.models import User


def ensure_resource_exists(
    data, status_code: int = 404, message: str = "Resource not found"
):
    if not data:
        raise HTTPException(status_code=status_code, detail=message)
    return data


def check_number_masters(user: User) -> Dict[str, Any]:
    """
    Перевіряє кількість майстрів у користувача та повертає їх.

    :param user: Об'єкт користувача з відношенням до майстрів
    :return: Словник з кількістю майстрів та їх списком
    """
    masters = user.masters
    if len(masters) > 1:
        raise HTTPException(
            status_code=409,
            detail={
                "count": len(masters),
                "masters": [
                    {"id": master.id, "name": master.name} for master in masters
                ],
            },
        )
    return masters[0]
