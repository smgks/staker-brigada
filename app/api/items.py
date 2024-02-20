from fastapi import APIRouter, Depends
from typing import List
from app.crud.items import get_categories, update_category, update_item

from app.dependencies.auth import UserDep
from app.dependencies.db import SessionDep
from app.crud import get_items, add_items, add_category, remove_items, remove_category
from app.schemas import NewItem, NewCategory, UpdateItem, UpdateCategory
from app.schemas.items import ItemCategory, ItemWithCategory


def token_dep(_: UserDep):
    pass


router = APIRouter(
    dependencies=[Depends(token_dep)]
)

@router.get("/", response_model=List[ItemWithCategory])
def items(
    db: SessionDep,
    from_id: int | None = None,
    page_size: int | None = 20,
):
    items = get_items(db, from_id, page_size)
    return [
        ItemWithCategory(
            class_name=i.class_name,
            item_id=i.id,
            category_id=i.category_id,
            category_name=i.category.name,
        ) for i in items
    ]

@router.delete("/")
def delete_items(
    db: SessionDep,
    ids: List[int],
):
    return remove_items(db, ids)

@router.post("/", response_model=List[ItemWithCategory])
def post_items(
    db: SessionDep,
    items: List[NewItem]
):
    new_items = add_items(
        db,
        items,
    )
    return [
        ItemWithCategory(
            class_name=i.class_name,
            item_id=i.id,
            category_id=i.category_id,
            category_name=i.category.name,
        ) for i in new_items
    ]

@router.get("/category", response_model=List[ItemCategory])
def categories(
    db: SessionDep,
):
    return get_categories(db)


@router.post("/category", response_model=ItemCategory)
def post_category(
    db: SessionDep,
    category: NewCategory,
):
    return add_category(db, category)


@router.delete("/category/{category_id}")
def delete_category(
    db: SessionDep,
    category_id: int,
):
    return remove_category(db, category_id)


@router.post("/{item_id}", response_model=UpdateItem)
def item_update(
    db: SessionDep,
    item_id: int,
    data: UpdateItem,
):
    return update_item(db, item_id, data)


@router.post("/category/{category_id}", response_model=UpdateCategory)
def category_update(
    db: SessionDep,
    category_id: int,
    data: UpdateCategory,
):
    return update_category(db, category_id, data)
