"""SQLAlchemyのモデルを定義."""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from .database import Base


class User(Base):
    """ユーザーのモデル.

    属性:   id (int): ユーザーの一意の識別子です。   name (str): ユーザーの名前です。
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class Room(Base):
    """ルームのモデル.

    属性:   id (int): ルームの一意の識別子です。   name (str): ルームの名前です。   capacity
    (int): ルームの収容人数です。
    """

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    capacity = Column(Integer)


class Booking(Base):
    """予約のモデル."""

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=False
    )
    room_id = Column(
        Integer, ForeignKey("rooms.id", ondelete="SET NULL"), nullable=False
    )
    booked_num = Column(Integer)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
