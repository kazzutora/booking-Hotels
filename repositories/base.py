from sqlalchemy import select

from src.schemas.hotels import Hotel


class BaseRepository:
    model = None
    def __init__(self, session):
        self.session = session

    async def get_all(self,*args,**kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model , from_attributes = True) for model in result.scalars().all()]

    async def get_one_or_none(self , **filter_by):
        query = select(self.model),filter_by(**filter_by)
        result = await self.session.execute(query)
        res = result.scalars().get_one_or_none()
        if res is None:
            return None
        return self.schema.model_validate(model)
