from datetime import datetime, date

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from repositories.base import BaseRepository
from repositories.hotels import HotelsRepository
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.schemas.bookings import BookingsAdd, Bookings
from src.schemas.rooms import Room, RoomAdd
from sqlalchemy import select, func, insert , delete , update


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Bookings

