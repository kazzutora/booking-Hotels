import asyncio
from time import sleep

from src.database import async_session_maker, async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task
def test_task():
    sleep(5)
    print('hello')


async def get_bookings_with_today_checkin_helper():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f'{bookings}')
@celery_instance.task(name='booking_today_checkin')
def booking_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())
