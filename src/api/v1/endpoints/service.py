import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.repository import crud
from db.models.service import Service
from db.models.user import User
from schemas import service
from decorators.permissions import requires_role
from core.dependencies import get_current_user, get_db
from utils.validators import ensure_resource_exists
from services.user.user_service import user_tools


router = APIRouter(prefix="/services", tags=["services"])
logger = logging.getLogger(__name__)


@router.get(
    "/", response_model=list[service.ServiceResponse], status_code=status.HTTP_200_OK
)
@requires_role(["master", "client", "master"])
async def get_services(
    master_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    filters = {}
    if user.role == "master":
        filters["master_id"] = user.id
    elif master_id is None:
        master = user_tools.check_number_masters(user)
        filters["master_id"] = master.id

    result = await crud.read(model=Service, session=db, **filters)
    services = result.unique().scalars().all()
    ensure_resource_exists(services)
    return services


@router.post(
    "/", response_model=service.ServiceCreate, status_code=status.HTTP_201_CREATED
)
@requires_role(["master"])
async def create_service(
    service: service.ServiceCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await crud.create(
        model=Service,
        session=db,
        name=service.name,
        price=service.price,
    )
    ensure_resource_exists(result, 422, "Invalid data provided to create the service")
    return result


@router.patch("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["master"])
async def update_service(
    service_id: int,
    service: service.ServiceUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    update_service = service.model_dump(exclude_unset=True)

    result = await crud.update(
        model=Service,
        session=db,
        expressions=(Service.id == service_id),
        **update_service,
    )
    ensure_resource_exists(result)


@router.patch("/deactivate/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["master"])
async def deactivate_service(
    service_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await crud.update(
        model=Service,
        session=db,
        expressions=(Service.id == service_id,),
        is_active=False,
    )
    ensure_resource_exists(result)
