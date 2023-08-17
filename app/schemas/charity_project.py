from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

FROM_TIME = datetime.now().isoformat(timespec='minutes')

TO_TIME = (datetime.now() + timedelta(days=1)).isoformat(timespec='minutes')


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = Field(None, example=1)


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt = Field(..., example=1)


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