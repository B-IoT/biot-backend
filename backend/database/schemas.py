from pydantic import BaseModel
from enum import Enum


class StatusEnum(str, Enum):
    available = "available"
    unavailable = "unavailable"


class BaseItem(BaseModel):
    type: str
    status: StatusEnum
    battery: int
    latitude: float
    longitude: float


class Item(BaseItem):
    id: int

    class Config:
        orm_mode = True