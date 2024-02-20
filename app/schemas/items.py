from typing import List
from pydantic import BaseModel, ConfigDict


class UpdateItem(BaseModel):
    class_name: str | None
    category_id: int | None
    
    model_config = ConfigDict(from_attributes=True)


class UpdateCategory(BaseModel):
    name: str | None

    model_config = ConfigDict(from_attributes=True)


class NewItem(BaseModel):
    class_name: str
    category_id: int


class NewCategory(BaseModel):
    category_name: str


class ItemWithCategory(BaseModel):
    class_name: str
    category_name: str
    item_id: int
    category_id: int


class SimpleItem(BaseModel):
    class_name: str
    id: int


class CategoryWithItems(BaseModel):
    category_name: str
    category_id: int
    items: List[SimpleItem]
    

class ItemCategory(BaseModel):
    name: str
    id: int

