"""Entityスキーマファイル."""

import datetime

from pydantic import BaseModel, Field


class Booking(BaseModel):
    """予約のスキーマ."""

    id: int
    room_id: int
    user_id: int
    booked_num: int
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime

    class Config:
        """設定"""

        orm_mode = True


class User(BaseModel):
    """ユーザーのスキーマ."""

    id: int
    name: str = Field(max_length=12)

    class Config:
        """設定"""

        orm_mode = True


class Room(BaseModel):
    """ルームのスキーマ."""

    id: int
    name: str = Field(max_length=12)
    capacity: int

    class Config:
        """設定"""

        orm_mode = True
