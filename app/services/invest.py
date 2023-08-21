from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def not_fully_invested(
    obj_in: Union[CharityProject, Donation],
    session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    objects = await session.execute(
        select(obj_in).where(obj_in.fully_invested == 0
                             ).order_by(obj_in.create_date)
    )
    return objects.scalars().all()


async def stop_donation(obj_in: Union[CharityProject, Donation]):
    obj_in.invested_amount = obj_in.full_amount
    obj_in.fully_invested = True
    obj_in.close_date = datetime.utcnow()
    return obj_in


async def invest_money(
    obj_create: Union[CharityProject, Donation],
    obj_in: Union[CharityProject, Donation],
) -> Union[CharityProject, Donation]:
    money_left_project = obj_create.full_amount - obj_create.invested_amount
    money_left_donation = obj_in.full_amount - obj_in.invested_amount

    if money_left_project > money_left_donation:
        obj_create.invested_amount += money_left_donation
        await stop_donation(obj_in)
    elif money_left_project == money_left_donation:
        await stop_donation(obj_create)
        await stop_donation(obj_in)
    else:
        obj_in.invested_amount += money_left_project
        await stop_donation(obj_create)

    return obj_create, obj_in


async def investment(obj_create: Union[CharityProject, Donation],
                     obj_in_db: Union[CharityProject, Donation],
                     session: AsyncSession
                     ) -> Union[CharityProject, Donation]:
    donations_left = await not_fully_invested(obj_in_db, session)
    for donation in donations_left:
        charity, donation = await invest_money(obj_create, donation)
        session.add(charity)
        session.add(donation)
    await session.commit()
    await session.refresh(obj_create)
    return obj_create