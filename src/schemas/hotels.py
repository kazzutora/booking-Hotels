from typing import Optional

from pydantic import BaseModel, Field , ConfigDict


class HotelAdd(BaseModel):
    title: str
    location: str

class Hotel(HotelAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)




class HotelPATCH(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None