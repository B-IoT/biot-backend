from pydantic import BaseModel, validator
from enum import Enum
from datetime import datetime


class StatusEnum(str, Enum):
    available = "available"
    unavailable = "unavailable"


class BaseItem(BaseModel):
    kontaktId: str
    status: StatusEnum = StatusEnum.available
    battery: int = 100
    latitude: float = 0
    longitude: float = 0
    lastEventTimestamp: datetime = datetime.utcnow()

    @validator("battery")
    def battery_must_be_in_range(cls, v):
        if v < 0 or v > 100:
            raise ValueError("The battery level must be between 0 and 100")

        return v


class TypedItem(BaseItem):
    type: str

    # TODO: define type as an Enum


class Item(BaseItem):
    id: int

    class Config:
        orm_mode = True