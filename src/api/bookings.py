from fastapi import APIRouter, Body

from repositories.bookings import BookingsRepository
from src.api.dependencies import DBDep, UserIdDep
from src.database import async_session_maker
from src.schemas.bookings import Bookings, BookingsAdd, BookingAddRequest

router = APIRouter(prefix='/bookings', tags=['Бронирование'])


@router.get('')
async def get_bookings(db:DBDep):
    return await db.bookings.get_all()
@router.get('/me')
async def get_me(user_id: UserIdDep ,db:DBDep):
    return await db.bookings.get_filtered(user_id=user_id)

@router.post('')
async def add_bookings(
        user_id: UserIdDep ,
        db: DBDep,
        booking_data: BookingAddRequest,
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int  = room.price
    _booking_data = BookingsAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.dict(),
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {'status': 'OK', 'data': booking}