"""Entityスキーマファイル."""

import datetime

from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    """予約作成用のスキーマ."""

    room_id: int
    user_id: int
    booked_num: int
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime

    class Config:
        """設定"""

        orm_mode = True


class UserCreate(BaseModel):
    """ユーザー作成用のスキーマ."""

    name: str = Field(max_length=12)


class RoomCreate(BaseModel):
    """ルーム作成用のスキーマ."""

    name: str = Field(max_length=12)
    capacity: int


class Booking(BookingCreate):
    """予約のスキーマ."""

    id: int

    class Config:
        """設定"""

        orm_mode = True


class User(UserCreate):
    """ユーザーのスキーマ."""

    id: int

    class Config:
        """設定"""

        orm_mode = True


class Room(RoomCreate):
    """ルームのスキーマ."""

    id: int

    class Config:
        """設定"""

        orm_mode = True
