from typing import Optional
from pydantic import BaseModel, Field , ConfigDict
from datetime import date
from src.models.bookings import BookingsOrm

class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date
# У файлі src/schemas/bookings.py

class BookingsAdd(BaseModel):
    room_id: int
    user_id: int
    date_from: date  # ← виправлено
    date_to: date
    price: float
class Bookings(BookingsAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)
