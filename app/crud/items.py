from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List
from app.errors import UniqueConstraintException
from app.errors.errors import ItemNotFound

from app.models import Item, Category
from app.schemas import NewItem, NewCategory
from app.schemas.items import UpdateCategory, UpdateItem


def get_items(
    db: Session,
    from_id: int | None,
    page_size: int | None,
) -> List[Item]:
    query = db.query(
        Item
    )
    if from_id:
        query.filter(
            Item.id >= from_id
        )
    query.order_by(
        Item.id,
    )
    if page_size:
        query.limit(
            page_size,
        )
    query.join(
        Category
    )
    return query.all()

def remove_items(
    db: Session,
    item_ids: List[int]
) -> int:
    count = db.query(Item).where(Item.id.in_(item_ids)).delete()
    db.commit()
    return count

def add_items(
    db: Session,
    new_items: List[NewItem]
) -> List[Item]:
    items = [
        Item(
            class_name=i.class_name,
            category_id=i.category_id,
        ) for i in new_items
    ]
    db.bulk_save_objects(
        items,
    )
    try:
        db.commit()
    except IntegrityError:
        raise UniqueConstraintException()

    return db.query(
        Item,
    ).join(
        Category,
    ).where(
        Item.category_id.in_([i.category_id for i in items]),
    ).all()


def get_categories(
    db: Session,
) -> List[Category]:
    return db.query(Category).all()


def add_category(
    db: Session,
    category: NewCategory,
) -> Category:
    _category = Category(
        name=category.category_name,
    )
    try: 
        db.add(_category)
        db.commit()
    except IntegrityError:
        raise UniqueConstraintException()
    
    db.refresh(_category)
    return _category


def remove_category(
    db: Session,
    category_id: int,
) -> int:
    count = db.query(Category).where(
        Category.id == category_id,
    ).delete()
    db.commit()
    return count

def update_item(
    db: Session,
    item_id: int,
    data: UpdateItem,
) -> Item:
    _item = db.query(Item).get(item_id)
    if _item is None:
        raise ItemNotFound()
    to_update = data.dict(exclude_unset=True)
    
    for key, value in to_update.items():
        setattr(_item, key, value)
    db.commit()
    db.refresh(_item)
    return Item


def update_category(
    db: Session,
    category_id,
    data: UpdateCategory,
):
    _category = db.query(Category).get(category_id)
    if _category is None:
        raise ItemNotFound()
    to_update = data.dict(exclude_unset=True)

    for key, value in to_update.items():
        setattr(_category, key, value)
    db.commit()
    db.refresh(_category)
    return _category
