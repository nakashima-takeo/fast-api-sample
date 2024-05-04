from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class ShopInfo(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    location: str | None = None


class Item(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    description: str | None = None
    price: int
    tax: float | None = None


class Data(BaseModel):
    shop_info: ShopInfo | None = None
    items: list[Item]


@app.get("/countries/")
async def country(country_name: str | None = None, country_no: int | None = None):
    return {"country_name": country_name, "country_no": country_no}


@app.post("/")
async def index(data: Data):
    return {"data": data}
