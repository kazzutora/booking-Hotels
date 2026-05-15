from typing import Optional
from pydantic import BaseModel, Field , ConfigDict


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str
    price: int
    quantity: int

class Hotel(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


