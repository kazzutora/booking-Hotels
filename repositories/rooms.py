from pydantic import BaseModel

from repositories.base import BaseRepository
from repositories.hotels import HotelsRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room, RoomAdd
from sqlalchemy import select, func, insert , delete , update

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(self,
                      title=None,
                      id=None,
                      description=None,
                      price=None,
                      quantity=None,
                      limit=100,
                      offset=0,
                      hotel_id=None):
        query = select(RoomsOrm)

        if description:
            query = query.filter(func.lower(RoomsOrm.description).contains(description.strip().lower()))
        if title:
            query = query.filter(func.lower(RoomsOrm.title).contains(title.strip().lower()))
        if price:
            query = query.filter(RoomsOrm.price == price)
        if quantity:
            query = query.filter(RoomsOrm.quantity == quantity)
        if hotel_id:
            query = query.filter(RoomsOrm.hotel_id == hotel_id)

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()

    # async def add(self, data : BaseModel):
    #     add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
    #     result = await self.session.execute(add_data_stmt)
    #     model = result
    #     return self.schema.model_validate(model, from_attributes=True)
    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        room = result.scalars().first()
        # Повертаємо словник або ORM об'єкт, але не корутину

        return room  # ← Важливо: return, а не await
    async def add(self, data) -> Room:
        """Добавление новой комнаты"""
        # Преобразуем данные в словарь, если это Pydantic модель
        if hasattr(data, 'model_dump'):
            data = data.model_dump()

        # Выполняем INSERT и получаем результат
        query = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(query)
        await self.session.commit()

        # Получаем объект ORM из результата
        room_orm = result.scalar_one()  # scalar_one() вместо simple object

        # Возвращаем Pydantic модель
        return self.schema.model_validate(room_orm)

    async def edit(self, data, exclude_unset: bool = False, **filter_by):
        # Сначала получаем словарь с данными, применяя exclude_unset к model_dump
        update_data = data.model_dump(exclude_unset=exclude_unset)
        # Затем применяем фильтрацию и обновление
        query = update(self.model).filter_by(**filter_by).values(**update_data)
        await self.session.execute(query)
        await self.session.commit()
    async def edit_patch(self, data: BaseModel ,skip_unset: bool = False,**filter_by) -> None:
        update_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=skip_unset))
        await self.session.execute(update_stmt)
    async def delete(self, **filter_by) -> None:
        query = delete(self.model).filter_by(**filter_by)
        await self.session.execute(query)



