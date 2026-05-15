from sqlalchemy.testing.schema import mapped_column
from sqlalchemy import String, ForeignKey
from src.database import Base
from sqlalchemy.orm import Mapped

class HotelsOrm(Base):
    __tablename__ = 'hotels'
    id: Mapped[int]= mapped_column(primary_key=True)
    title: Mapped[str]= mapped_column(String(length=100))
    location: Mapped[str]= mapped_column(String(length=100))

