from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, HTTPException, status, Response, Request, Query, Body
from passlib.context import CryptContext
import jwt

from repositories.rooms import RoomsRepository
from repositories.users import UserRepository
from src.api.dependencies import UserIdDep, PaginationDep
from src.config import settings
from src.database import async_session_maker
from src.schemas.rooms import RoomAdd, Room
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/rooms", tags=["Комнаты отелей"])

@router.get('')
async def get_rooms(pagination: PaginationDep,
            title: str | None = Query(None, description="Название отеля"),
            id: int | None = Query(None, description="ID:" ) ,
            description: str | None = Query(None , description="Описание"  ),
            price: int | None = Query(None, description="Цена :"  ),
            quantity: int | None = Query(None, description="Количество:",),
            hotel_id: int | None = Query(None, description="Отель:")
              ):
    per_page = pagination.per_page or 5

    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            title=title,
            id=id,
            description=description,
            price=price,
            quantity=quantity,
            hotel_id=hotel_id,
            limit=per_page,
            offset=per_page * (pagination.page - 1))


@router.post('', response_model=Room, status_code=status.HTTP_201_CREATED)
async def create_room(room_data: RoomAdd):
    """Создание новой комнаты"""
    async with async_session_maker() as session:
        # Проверяем, существует ли отель
        from repositories.hotels import HotelsRepository

        hotel = await HotelsRepository(session).get_one(id=room_data.hotel_id)
        if not hotel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Отель с ID {room_data.hotel_id} не найден"
            )

        # Создаем комнату
        room = await RoomsRepository(session).add(room_data)
        return room