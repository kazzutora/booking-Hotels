from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from src.database import Base
from src.models.facilities import FacilitiesOrm


class RoomsOrm(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    price: Mapped[int] = mapped_column()
    quantity: Mapped[int] = mapped_column()
    facilities : Mapped[list['FacilitiesOrm']] = relationship(
        back_populates="rooms",
        secondary = 'rooms_facilities',
    )