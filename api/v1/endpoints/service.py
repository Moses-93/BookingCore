from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from db.crud import crud
from db.models import Service, User
from schemas import service
from decorators.permissions import requires_role
from core.dependencies import verify_user, get_db


router = APIRouter(prefix="/services", tags=["services"])


@router.get("/", response_model=list[service.ServiceResponse])
@requires_role(["admin", "user"])
async def get_services(
    db: AsyncSession = Depends(get_db), user: User = Depends(verify_user)
):
    services = await crud.read(model=Service, session=db)
    return services


@router.post(
    "/", response_model=service.ServiceCreate, status_code=status.HTTP_201_CREATED
)
@requires_role(["admin"])
async def create_service(
    service: service.ServiceCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_user),
):
    result = await crud.create(
        model=Service,
        session=db,
        name=service.name,
        price=service.price,
        duration=service.duration,
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create service"
        )
    return result


@router.patch("/{service_id}", status_code=status.HTTP_200_OK)
@requires_role(["admin"])
async def update_service(
    service_id: int,
    service: service.ServiceUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_user),
):
    update_service = service.model_dump(exclude_unset=True)
    if not update_service:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update",
        )
    result = await crud.update(
        model=Service,
        session=db,
        expressions=(Service.id == service_id),
        **update_service
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found"
        )
    return {"detail": "Service updated successfully"}


@router.delete("/{service_id}", status_code=status.HTTP_200_OK)
@requires_role(["admin"])
async def delete_service(
    service_id: int,
    user: User = Depends(verify_user),
    db: AsyncSession = Depends(get_db),
):
    result = await crud.delete(model=Service, session=db, id=service_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Date not found"
        )
    return {"detail": "Date deleted successfully"}
