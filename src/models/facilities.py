from sqlalchemy.testing.schema import mapped_column
from sqlalchemy import String, ForeignKey
from src.database import Base
from sqlalchemy.orm import Mapped, relationship


# ВИДАЛІТЬ цей рядок:
# from src.models.rooms import RoomsOrm


class FacilitiesOrm(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    # Використовуйте рядок замість прямого імпорту
    rooms: Mapped[list['RoomsOrm']] = relationship(
        back_populates="facilities",
        secondary='rooms_facilities',
    )


class RoomsFacilitiesOrm(Base):
    __tablename__ = "rooms_facilities"

    # Зазвичай для зв'язкової таблиці NOT потрібен окремий id
    # Краще використовувати складовий первинний ключ
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'), primary_key=True)
    facility_id: Mapped[int] = mapped_column(ForeignKey('facilities.id'), primary_key=True)