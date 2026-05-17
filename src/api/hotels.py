
from operator import or_
from fastapi import Query, APIRouter, Body, HTTPException ,Depends
from sqlalchemy import insert, select, func
from starlette import status

from repositories.hotels import HotelsRepository
from repositories.rooms import RoomsRepository
from src.api.dependencies import PaginationDep, DBDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/hotels", tags=["Отели"])




@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Локацияя1z1"),
        title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
            location = location,
            title = title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
                               )

@router.get("/{hotel_id}")
async def get_hotel_by_id(
        hotel_id: int
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one(id=hotel_id)
        if hotel is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Готель з ID {hotel_id} не знайдено"
            )
        return hotel




@router.post("")
async def create_hotel(hotel_data: HotelAdd = Body()):  # добавил ()
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)  # передал аргумент
        await session.commit()
        return {'status': 'OK', 'data': hotel}
# Строчка данных про добавление отеля в базу данных(После вставки данных результат)


@router.put("/{hotel_id}")
async def edit_hotel(
        hotel_id: int,
        hotel_data: HotelAdd,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data , id=hotel_id)  # только session
        await session.commit()
    return {'status': 'OK'}

@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отел",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
async def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit_patch(hotel_data, skip_unset=True , id=hotel_id)
        await session.commit()
    return {'status': 'OK'}

@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "success", "message": f"Отель с ID {hotel_id} успешно удалён"}
