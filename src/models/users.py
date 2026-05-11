from sqlalchemy.testing.schema import mapped_column
from sqlalchemy import String, ForeignKey
from src.database import Base
from sqlalchemy.orm import Mapped

class UsersOrm(Base):
    __tablename__ = 'users'


    id: Mapped[int]= mapped_column(primary_key=True)
    email: Mapped[str]= mapped_column(String(length=100) , unique=True , nullable=False)
    hashed_password: Mapped[str]= mapped_column(String(length=100))
