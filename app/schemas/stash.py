from typing import List
from pydantic import BaseModel


class PositionSchema(BaseModel):
    x: float
    y: float
    z: float
    x_dir: float
    y_dir: float
    z_dir: float


class StashesSchema(BaseModel):
    id: int
    tier: int
    class_name: str
    avg_items_points: int
    position: PositionSchema


class StashItemSchema(BaseModel):
    item_id: int
    class_name: str


class StashInfoItemSchema(BaseModel):
    item_id: int
    stash_id: int
    points: int
    class_name: str
    chance_multiplayer: float


class StashInfoSchema(BaseModel):
    id: int
    tier: int
    class_name: str
    position: PositionSchema
    avg_items_points: int
    items: List[StashInfoItemSchema]


class StashItemsSchema(BaseModel):
    id: int
    tier: int
    class_name: str
    avg_items_points: int
    items: List[StashItemSchema]


class CreateStashItem(BaseModel):
    item_id: int
    stash_id: int
    chance_multiplayer: float | None = None
    points: int


class CreateStash(BaseModel):
    tier: int
    class_name: str
    position: PositionSchema
    avg_items_points: int

