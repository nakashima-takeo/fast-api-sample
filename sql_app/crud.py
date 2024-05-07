"""CRUD 操作を行うモジュール."""

from sqlalchemy.orm import Session

from . import models, schemas


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.User]:
    """データベースからユーザーを取得します。

    Args:
      db (Session): データベースセッション
      skip (int, optional): スキップするレコード数. Defaults to 0.
      limit (int, optional): 取得する最大レコード数. Defaults to 100.

    Returns:
      List[User]: ユーザーのリスト
    """
    result = db.query(models.User).offset(skip).limit(limit).all()
    return [schemas.User(id=user.id, name=user.name) for user in result]


def get_rooms(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.Room]:
    """データベースからルームを取得します。

    Args:
      db (Session): データベースセッション
      skip (int, optional): スキップするレコード数. Defaults to 0.
      limit (int, optional): 取得する最大レコード数. Defaults to 100.

    Returns:
      List[Room]: ルームのリスト
    """
    result = db.query(models.Room).offset(skip).limit(limit).all()
    return [
        schemas.Room(id=room.id, name=room.name, capacity=room.capacity)
        for room in result
    ]


def get_bookings(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.Booking]:
    """データベースからブッキングを取得します。

    Args:
      db (Session): データベースセッション
      skip (int, optional): スキップするレコード数. Defaults to 0.
      limit (int, optional): 取得する最大レコード数. Defaults to 100.

    Returns:
      List[Booking]: ブッキングのリスト
    """
    result = db.query(models.Booking).offset(skip).limit(limit).all()
    return [
        schemas.Booking(
            id=booking.id,
            room_id=booking.room_id,
            user_id=booking.user_id,
            booked_num=booking.booked_num,
            start_datetime=booking.start_time,
            end_datetime=booking.end_time,
        )
        for booking in result
    ]


def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    """ユーザーを作成します。

    Args:
      db (Session): データベースセッション
      user (User): 作成するユーザーの情報

    Returns:
      User: 作成されたユーザー
    """
    db_user = models.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_room(db: Session, room: schemas.RoomCreate) -> schemas.Room:
    """ルームを作成します。

    Args:
      db (Session): データベースセッション
      room (Room): 作成するルームの情報

    Returns:
      Room: 作成されたルーム
    """
    db_room = models.Room(name=room.name, capacity=room.capacity)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def create_booking(db: Session, booking: schemas.BookingCreate) -> schemas.Booking:
    """ブッキングを作成します。

    Args:
      db (Session): データベースセッション
      booking (Booking): 作成するブッキングの情報

    Returns:
      Booking: 作成されたブッキング
    """
    db_booking = models.Booking(
        room_id=booking.room_id,
        user_id=booking.user_id,
        booked_num=booking.booked_num,
        start_time=booking.start_datetime,
        end_time=booking.end_datetime,
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    res = schemas.Booking(
        id=db_booking.id,
        room_id=db_booking.room_id,
        user_id=db_booking.user_id,
        booked_num=db_booking.booked_num,
        start_datetime=db_booking.start_time,
        end_datetime=db_booking.end_time,
    )
    return res
