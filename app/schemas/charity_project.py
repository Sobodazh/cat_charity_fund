from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

AMOUNT_DAYS_FOR_EXAMPLE = 1
FROM_TIME = datetime.utcnow().isoformat(timespec='minutes')
TO_TIME = ((datetime.utcnow() +
            timedelta(days=AMOUNT_DAYS_FOR_EXAMPLE)).isoformat(timespec='minutes'))
FOR_EXAMPLE = 1
MIN_LENGHT = 1
MAX_LENGHT = 100


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=MIN_LENGHT, max_length=MAX_LENGHT)
    description: Optional[str] = Field(None, min_length=MIN_LENGHT)
    full_amount: Optional[PositiveInt] = Field(None, example=FOR_EXAMPLE)


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=MIN_LENGHT, max_length=MAX_LENGHT)
    description: str = Field(..., min_length=MIN_LENGHT)
    full_amount: PositiveInt = Field(..., example=FOR_EXAMPLE)


class CharityProjectUpdate(CharityProjectBase):
    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым!')
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime] = Field(None, example=FROM_TIME)
    close_date: Optional[datetime] = Field(None, example=TO_TIME)

    class Config:
        orm_mode = True