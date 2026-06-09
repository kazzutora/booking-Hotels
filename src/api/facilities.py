import json
from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache
from src.api.dependencies import DBDep
from src.connectors.redis_connector import RedisManager
from src.init import redis_manager
from src.schemas.facilities import Facilities, FacilitiesBase
from src.tasks.tasks import test_task

router = APIRouter(prefix='/facilities', tags=['Удобства'])


@router.get('')
@cache(expire=10)
async def get_bookings(db: DBDep):
    # Получаем данные из Redis
    
    facilities_from = await redis_manager.get('facilities')
    print(f'facilities_from: {facilities_from}')

    if not facilities_from:
        # Получаем из базы данных
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)

        # Сохраняем в Redis (исправлено!)
        await redis_manager.set('facilities', facilities_json, expire=3600)  # expire через 1 час

        return facilities
    else:
        # Возвращаем из Redis (нужно распарсить JSON)
        return json.loads(facilities_from)


@router.post('')
async def add_bookings(
        db: DBDep,
        facilities_data: FacilitiesBase,
):
    title: str = facilities_data.title
    _facilities_data = FacilitiesBase(
        title=title
    )
    facilities = await db.facilities.add(_facilities_data)
    await db.commit()
    test_task.delay()
    # После добавления новых удобств - очищаем кеш Redis
    await redis_manager.delete('facilities')

    return {'status': 'OK', 'data': facilities}