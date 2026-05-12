from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, HTTPException, status , Response , Request
from passlib.context import CryptContext
import jwt
from repositories.users import UserRepository
from src.api.dependencies import UserIdDep
from src.config import settings
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и автентификация"])

@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login_user(data: UserRequestAdd ,
                     response:Response):
    async with async_session_maker() as session:
        # Передаем email и hashed_password отдельно
        user = await UserRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Польвозователь з таким email не зарегистрирован ")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = AuthService().create_access_token({'user_id': user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
@router.patch('/logout', status_code=status.HTTP_200_OK)
async def logout_user(response: Response , user: UserIdDep):
    if not user:
        raise HTTPException(status_code=401, detail="Вы не авторизированые")
    response.delete_cookie("access_token")
    return {'status': 'Вы выйшли из системы'}

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(data: UserRequestAdd):
    # Хэшируем пароль
    hashed_password = AuthService().hash_password(data.password)

    async with async_session_maker() as session:
        # Передаем email и hashed_password отдельно
        await UserRepository(session).add(
            email=data.email,
            hashed_password=hashed_password
        )
        await session.commit()

    return {"status": "OK"}

@router.get('/only_auth')
async def only_auth(user_id: UserIdDep):
    async with async_session_maker() as session:
        user = await UserRepository(session).get_one_or_none(id=user_id)
    return user