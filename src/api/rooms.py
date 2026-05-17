from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, HTTPException, status, Response, Request, Query, Body
from passlib.context import CryptContext
import jwt

from repositories.rooms import RoomsRepository
from repositories.users import UserRepository
from src.api.dependencies import UserIdDep, PaginationDep
from src.config import settings
from src.database import async_session_maker
from src.schemas.rooms import RoomAdd, Room, RoomPATCH, RoomAddRequest, RoomPatchRequest
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        # Используем get_all вместо get_one
        rooms = await RoomsRepository(session).get_all(
            title=None,
            id=None,
            description=None,
            price=None,
            quantity=None,
            limit=100,  # задайте значения по умолчанию
            offset=0,
            hotel_id=hotel_id  # передаем hotel_id для фильтрации
        )
        return rooms


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
):
    _room_data = RoomPATCH(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}
