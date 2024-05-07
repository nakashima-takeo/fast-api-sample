# flake8: noqa: B008
"""FastAPI application for the booking system."""

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    """データベースセッションを取得します。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def index():
    """ルートエンドポイントのハンドラ関数です。

    Returns:
      dict: レスポンスメッセージを含む辞書オブジェクト
    """
    return {"message": "Success"}


# Read
@app.get("/users", response_model=list[schemas.User])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ユーザーを作成します。

    Args:
      user (User): 作成するユーザーの情報

    Returns:
      dict: 作成されたユーザーの情報
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/rooms", response_model=list[schemas.Room])
async def get_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ルームを作成するエンドポイントです。

    Args:
      room (Room): 作成するルームの情報

    Returns:
      dict: 作成されたルームの情報
    """
    rooms = crud.get_rooms(db, skip=skip, limit=limit)
    return rooms


@app.get("/bookings", response_model=list[schemas.Booking])
async def get_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ブッキングを作成するエンドポイントです。

    Args:
      booking (Booking): 作成するブッキングの情報

    Returns:
      dict: 作成されたブッキングの情報
    """
    bookings = crud.get_bookings(db, skip=skip, limit=limit)
    return bookings


# Create
@app.post("/users", response_model=schemas.User)
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    """ユーザーを作成します。

    Args:
      user (User): 作成するユーザーの情報

    Returns:
      dict: 作成されたユーザーの情報
    """
    return crud.create_user(db, user)


@app.post("/rooms", response_model=schemas.Room)
async def create_rooms(room: schemas.Room, db: Session = Depends(get_db)):
    """ルームを作成するエンドポイントです。

    Args:
      room (Room): 作成するルームの情報

    Returns:
      dict: 作成されたルームの情報
    """
    return crud.create_room(db, room)


@app.post("/bookings", response_model=schemas.Booking)
async def create_bookings(booking: schemas.Booking, db: Session = Depends(get_db)):
    """ブッキングを作成するエンドポイントです。

    Args:
      booking (Booking): 作成するブッキングの情報

    Returns:
      dict: 作成されたブッキングの情報
    """
    return crud.create_booking(db, booking)
