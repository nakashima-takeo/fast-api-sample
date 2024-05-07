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
    """予約のモデル.

    属性:   id (int): 予約の一意の識別子です。   user_id (int): 予約を行ったユーザーの識別子です。
    room_id (int): 予約されたルームの識別子です。   start_time (datetime): 予約の開始時間です。
    end_time (datetime): 予約の終了時間です。   created_at (datetime):
    予約が作成されたタイムスタンプです。   updated_at (datetime): 予約が最後に更新されたタイムスタンプです。
    """

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
