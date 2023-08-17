from datetime import datetime
from typing import Type

from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base_model import BaseModel


async def sum_calc(obj_create: BaseModel, obj_in: BaseModel):
    money_left_project = obj_create.full_amount - obj_create.invested_amount
    money_left_donation = obj_in.full_amount - obj_in.invested_amount
    if money_left_project > money_left_donation:
        obj_create.invested_amount += money_left_donation
        obj_in.invested_amount = obj_in.full_amount
        obj_in.fully_invested = True
        obj_in.close_date = datetime.now()
    elif money_left_project == money_left_donation:
        obj_create.invested_amount = obj_create.full_amount
        obj_in.invested_amount = obj_in.full_amount
        obj_in.fully_invested = True
        obj_create.fully_invested = True
        obj_in.close_date = datetime.now()
        obj_create.close_date = datetime.now()
    else:
        obj_in.invested_amount += money_left_project
        obj_create.invested_amount = obj_create.full_amount
        obj_create.fully_invested = True
        obj_create.close_date = datetime.now()
    return obj_create, obj_in


async def investment(
        obj_create: BaseModel,
        obj_in_db: Type[BaseModel],
        session: AsyncSession):
    donations_left = await session.execute(
        select(obj_in_db).where(
            obj_in_db.fully_invested == 0).order_by(
            asc(obj_in_db.create_date)
        )
    )
    donations_left = donations_left.scalars().all()
    for donation in donations_left:
        charity, donation = await sum_calc(obj_create, donation)
        session.add(charity)
        session.add(donation)
    await session.commit()
    await session.refresh(obj_create)
    return obj_create