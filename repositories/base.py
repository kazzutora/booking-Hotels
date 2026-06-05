from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete

from src.models.facilities import RoomsFacilitiesOrm
from src.schemas.facilities import RoomFacility, RoomFacilityAdd
from src.schemas.hotels import Hotel


class BaseRepository:
    model = None
    def __init__(self, session):
        self.session = session

    async def get_all(self,*args,**kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model , from_attributes = True) for model in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        res = result.scalar_one_or_none()

        if res is None:
            return None

        return self.schema.model_validate(res)

    async def add(self, data):
        """Додає новий запис"""
        orm_obj = self.model(**data.dict())
        self.session.add(orm_obj)
        await self.session.flush()
        return orm_obj

    async def add_bulk(self, data: list[BaseModel]):
       add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
       await self.session.execute(add_data_stmt)

    async def delete_by_room_id(self, room_id: int):
        """Видаляє всі зручності для кімнати"""
        query = delete(RoomsFacilitiesOrm).where(RoomsFacilitiesOrm.room_id == room_id)
        await self.session.execute(query)

    async def update_room_facilities(self, room_id: int, facilities_ids: list[int]):
        """Оновлює зручності кімнати"""
        # Видаляємо старі
        await self.delete_by_room_id(room_id)

        # Додаємо нові
        if facilities_ids:
            facilities_data = [
                RoomFacilityAdd(room_id=room_id, facility_id=f_id)
                for f_id in facilities_ids
            ]
            await self.add_bulk(facilities_data)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)
    async def get_filtered(self,*filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)

        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_by_id(self, record_id: int):
        """Базовий метод отримання запису за ID"""
        query = select(self.model).where(self.model.id == record_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)