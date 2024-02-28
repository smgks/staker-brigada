from pydantic import BaseModel, ConfigDict
from typing import List


class SimpleItem(BaseModel):
    class_name: str
    id: int

    model_config = ConfigDict(from_attributes=True)


class TraderInventoryItems(BaseModel):
    id: int | None
    skin_name: str
    vest: SimpleItem | None
    backpack: SimpleItem | None
    top: SimpleItem | None
    belt: SimpleItem | None
    legs: SimpleItem | None
    head: SimpleItem | None
    face: SimpleItem | None
    eyes: SimpleItem | None
    gloves: SimpleItem | None
    feet: SimpleItem | None
    armband: SimpleItem | None

    model_config = ConfigDict(from_attributes=True)


class TraderSpawnPosition(BaseModel):
    id: int | None
    x: float
    y: float
    z: float
    x_dir: float
    y_dir: float
    z_dir: float

    model_config = ConfigDict(from_attributes=True)


class TraderSpawn(BaseModel):
    id: int
    name: str
    items: TraderInventoryItems | None
    pos: TraderSpawnPosition | None

    model_config = ConfigDict(from_attributes=True)


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
    id: int
    steamid: str

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

