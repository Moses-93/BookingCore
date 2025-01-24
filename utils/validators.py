from fastapi import HTTPException


def ensure_resource_exists(
    data, status_code: int = 404, message: str = "Resource not found"
):
    if not data:
        raise HTTPException(status_code=status_code, detail=message)
    return data
