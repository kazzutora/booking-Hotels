from typing import Optional

from pydantic import BaseModel, Field


class HotelAdd(BaseModel):
    title: str
    location: str

class Hotel(HotelAdd):
    id: int




class HotelPATCH(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None