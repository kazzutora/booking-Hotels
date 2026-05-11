from pydantic import EmailStr
from sqlalchemy import select

from repositories.base import BaseRepository
from src.models.users  import UsersOrm
from src.schemas.users import User, UserWithHashedPassword


class UserRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def add(self, email: str, hashed_password: str):  # Два параметра
        """Добавление пользователя"""
        user = UsersOrm(email=email, hashed_password=hashed_password)
        self.session.add(user)
        return user
    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email = email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model)
