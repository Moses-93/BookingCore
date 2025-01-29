import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud import crud
from db.models import Service, User
from schemas import service
from decorators.permissions import requires_role
from core.dependencies import verify_user, get_db
from utils.validators import check_number_masters, ensure_resource_exists


router = APIRouter(prefix="/services", tags=["services"])
logger = logging.getLogger(__name__)


@router.get(
    "/", response_model=list[service.ServiceResponse], status_code=status.HTTP_200_OK
)
@requires_role(["admin", "user"])
async def get_services(
    master_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_user),
):
    if master_id is None:
        master = check_number_masters(user)
        master_id = master.id

    result = await crud.read(model=Service, session=db, master_id=master_id)
    services = result.unique().scalars().all()
    ensure_resource_exists(services)
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
    ensure_resource_exists(result, 400, "Invalid data provided to create the service")
    return result


@router.patch("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["admin"])
async def update_service(
    service_id: int,
    service: service.ServiceUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_user),
):
    update_service = service.model_dump(exclude_unset=True)

    result = await crud.update(
        model=Service,
        session=db,
        expressions=(Service.id == service_id),
        **update_service,
    )
    ensure_resource_exists(result)


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["admin"])
async def delete_service(
    service_id: int,
    user: User = Depends(verify_user),
    db: AsyncSession = Depends(get_db),
):
    result = await crud.delete(model=Service, session=db, id=service_id)
    ensure_resource_exists(result)
