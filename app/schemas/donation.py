from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

FROM_TIME = datetime.now().isoformat(timespec='minutes')

TO_TIME = (datetime.now() + timedelta(days=1)).isoformat(timespec='minutes')


class DonationCreate(BaseModel):
    full_amount: PositiveInt = Field(..., example=1)
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationDB(DonationCreate):
    id: int
    create_date: Optional[datetime] = Field(None, example=FROM_TIME)

    class Config:
        orm_mode = True


class DonationDBFull(DonationDB):
    id: int
    create_date: Optional[datetime] = Field(None, example=FROM_TIME)
    user_id: Optional[int]
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    close_date: Optional[datetime] = Field(None, example=TO_TIME)