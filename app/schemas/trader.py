from pydantic import BaseModel, ConfigDict
from typing import List


class TraderItem(BaseModel):
    id: int
    class_name: str
    price: int | None
    sell_price: int | None
    count: int | None

    model_config = ConfigDict(from_attributes=True)


class TraderCategory(BaseModel):
    category_name: str
    items: List[TraderItem]

    model_config = ConfigDict(from_attributes=True)


class TraderShop(BaseModel):
    name: str
    categories: List[TraderCategory]

    model_config = ConfigDict(from_attributes=True)


class TraderBuyItem(BaseModel):
    class_name: str
    count: int

    model_config = ConfigDict(from_attributes=True)


class TraderShopCart(BaseModel):
    items: List[TraderItem]

    model_config = ConfigDict(from_attributes=True)

