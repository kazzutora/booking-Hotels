from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1)]  # убираем None, ставим int
    per_page: Annotated[int, Query(5, ge=1, lt=30)]  # меняем None на 5


PaginationDep = Annotated[PaginationParams, Depends()]