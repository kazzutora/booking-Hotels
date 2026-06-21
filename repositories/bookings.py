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
from repositories.mappers.base import DataMapper

class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Bookings

    async def get_bookings_with_today_checkin(self):
        query = select(BookingsOrm).filter(BookingsOrm.date_from == date.today())
        res = await self.session.execute(query)
        return [Bookings.model_validate(booking, from_attributes=True)
                for booking in res.scalars().all()]