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
                      title,id,
                      description,
                      price,
                      quantity,
                      limit,
                      offset,
                      hotel_id ):
        query = select(RoomsOrm)
        if description:
            query = query.filter(func.lower(RoomsOrm.description).contains(description.strip().lower()))

        if title:
            query = query.filter(func.lower(RoomsOrm.title).contains(title.strip().lower()))
        if price:
            query = query.filter(RoomsOrm.price == price )
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

