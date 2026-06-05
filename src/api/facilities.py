from fastapi import APIRouter, Body
from src.api.dependencies import DBDep

from src.schemas.facilities import Facilities, FacilitiesBase

router = APIRouter(prefix='/facilities', tags=['Удобства'])

@router.get('')
async def get_bookings(db:DBDep):
    return await db.facilities.get_all()

@router.post('')
async def add_bookings(
        db: DBDep,
        facilities_data: FacilitiesBase,
):
    title: str = facilities_data.title
    _facilities_data = FacilitiesBase(
        title = title
    )
    facilities = await db.facilities.add(_facilities_data)
    await db.commit()
    return {'status': 'OK', 'data': facilities}

    #
    # _booking_data = BookingsAdd(
    #     user_id=user_id,
    #     price=room_price,
    #     **booking_data.dict(),
    # )
    # booking = await db.bookings.add(_booking_data)
    # await db.commit()
    # return {'status': 'OK', 'data': booking}