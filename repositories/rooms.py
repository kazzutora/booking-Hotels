from datetime import date

from pydantic import BaseModel

from repositories.base import BaseRepository
from repositories.hotels import HotelsRepository
from src.database import engine
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room, RoomAdd
from sqlalchemy import select, func, insert , delete , update

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
    ):
        """
        with rooms_count as (
            select room_id, count(*) as rooms_booked from bookings
            where date_from <= '2024-11-07' and date_to >= '2024-07-01'
            group by room_id
        ),
        rooms_left_table as (
            select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
            from rooms
            left join rooms_count on rooms.id = rooms_count.room_id
        )
        select * from rooms_left_table
        where rooms_left > 0;
        """

        """
        !select room_id, count(*) as rooms_booked from bookings
            where date_from <= '2024-11-07' and date_to >= '2024-07-01'
            group by room_id
        """
        rooms_count = (
            select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from <= date_to,
                BookingsOrm.date_to >= date_from,
            )
            .group_by(BookingsOrm.room_id)
            .cte(name="rooms_count")
        )

        """
        rooms_left_table as (
            select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
            from rooms
            left join rooms_count on rooms.id = rooms_count.room_id
        )
        """
        rooms_left_table = (
            select(
                RoomsOrm.id.label("room_id"),
                (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
            .cte(name="rooms_left_table")
        )

        """
        !select * from rooms_left_table
        where rooms_left > 0
        """
        rooms_ids_for_hotel = (
            select(RoomsOrm.id)
            .select_from(RoomsOrm)
            .filter_by(hotel_id=hotel_id)
            .subquery(name='rooms_ids_for_hotel')
        )

        rooms_ids_to_get = (
            select(rooms_left_table.c.room_id)
            .select_from(rooms_left_table)
            .filter(
                rooms_left_table.c.rooms_left > 0,
                rooms_left_table.c.room_id.in_(rooms_ids_for_hotel),
            )
        )

        print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))



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





