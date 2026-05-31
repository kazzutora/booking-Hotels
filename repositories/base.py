from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
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

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)