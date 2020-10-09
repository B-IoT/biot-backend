from pydantic import BaseModel
from enum import Enum


class StatusEnum(str, Enum):
    available = "available"
    unavailable = "unavailable"


class Item(BaseModel):
    id: int
    type: str
    status: StatusEnum
    battery: int
    latitude: float
    longitude: float

    class Config:
        orm_mode = True