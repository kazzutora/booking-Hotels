from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, HTTPException, status , Response , Request
from passlib.context import CryptContext
import jwt
from repositories.users import UserRepository
from src.api.dependencies import UserIdDep, PaginationDep
from src.config import settings
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/rooms", tags=["Комнаты отелей"])

@router.get('')
def get_rooms(pagination: PaginationDep,
            title: str | None = Query(None, description="Название отеля")
              )
    per_page = pagination.per_page or 5

    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1))