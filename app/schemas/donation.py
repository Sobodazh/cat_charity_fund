from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

AMOUNT_DAYS_FOR_EXAMPLE = 1
FROM_TIME = datetime.utcnow().isoformat(timespec='minutes')

TO_TIME = ((datetime.utcnow() +
            timedelta(days=AMOUNT_DAYS_FOR_EXAMPLE)).isoformat(timespec='minutes'))
FOR_EXAMPLE = 1


class DonationCreate(BaseModel):
    full_amount: PositiveInt = Field(..., example=FOR_EXAMPLE)
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