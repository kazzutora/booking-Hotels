from fastapi.params import Body
from pydantic import BaseModel

from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func, insert , delete , update

from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(self,
                      location,
                      title,
                      limit,
                      offset):
        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))

        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
            query = (
                query
                .limit(limit)
                .offset(offset)
            )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]


    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        hotel = result.scalars().first()
        # Повертаємо словник або ORM об'єкт, але не корутину

        return hotel  # ← Важливо: return, а не await


    async def add(self, data: BaseModel):  # убрал Body
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result  = await self.session.execute(add_data_stmt)
        model = result.scalar()
        return self.schema.model_validate(model, from_attributes=True)

    async def edit(self , data: BaseModel ,**filter_by) -> None:
        # 1. Находим запись по фильтрам
        query = update(self.model).filter_by(**filter_by).values(**data.model_dump())
        await self.session.execute(query)
    async def edit_patch(self, data: BaseModel ,skip_unset: bool = False,**filter_by) -> None:
        update_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=skip_unset))
        await self.session.execute(update_stmt)


    async def delete(self, **filter_by) -> None:
        query = delete(self.model).filter_by(**filter_by)
        await self.session.execute(query)





