from pydantic import ConfigDict, BaseModel

from src.database import Base


class FacilitiesBase(BaseModel):
    title: str
    model_config = ConfigDict(from_attributes=True)


class Facilities(FacilitiesBase):
    id: int


class RoomFacilityAdd(BaseModel):
    room_id : int
    facility_id: int

class RoomFacility(RoomFacilityAdd):
    id : int
