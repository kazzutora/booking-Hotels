from repositories.base import BaseRepository
from src.models.hotels import RoomOrm


class RoomsRepository(BaseRepository):
    model = RoomOrm