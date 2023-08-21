from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_name_duplicate, check_project_exists,
                                closed_project, donations_exists,
                                new_sum_less_invested_amount)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import project_crud
from app.models import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.invest import investment

router = APIRouter()


@router.post('/',
             response_model=CharityProjectDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)])
async def create_new_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(project.name, session)
    new_project = await project_crud.create(project, session)
    await investment(new_project, Donation, session)
    return new_project


@router.get('/',
            response_model=List[CharityProjectDB],
            response_model_exclude_none=True)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session)
):
    return await project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    await closed_project(project_id, session)
    project = await check_project_exists(project_id, session)
    if obj_in.full_amount is not None:
        await new_sum_less_invested_amount(obj_in.full_amount, project_id, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    project = await project_crud.update(
        project, obj_in, session
    )
    await investment(project, Donation, session)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(
        project_id, session
    )
    await donations_exists(project_id, session)
    return await project_crud.remove(
        project, session
    )