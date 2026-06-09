from typing import Optional
from pydantic import BaseModel, Field , ConfigDict

from src.schemas.facilities import Facilities


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str
    price: int
    quantity: int
class RoomPATCH(BaseModel):
    title: Optional[str] = None
    hotel_id: Optional[int] = None
    description: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None

class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int]  = []
class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []

class Room(RoomAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)

class RoomWithRels(Room):
    facilities: list[Facilities] = []


