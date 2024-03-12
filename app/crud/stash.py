from typing import List
from sqlalchemy.orm import Session
from app.models import Stash, Position
from app.models.game import StashItem, Item
from app.schemas.stash import CreateStash, CreateStashItem


def get_stashes(db: Session) -> List[Stash]:
    query = db.query(Stash)
    query.join(Position)
    return query.all()


def spawn_stash_base(db: Session, stash: int) -> Stash:
    query = db.query(Stash)
    query.join(Position)
    query.join(StashItem)
    query.join(Item)
    query.where(Stash.id == stash)
    return query.first()


def create_stash(db: Session, stash: CreateStash) -> Stash:
    position = Position(
        x=stash.position.x,
        y=stash.position.y,
        z=stash.position.z,
        x_dir=stash.position.x_dir,
        y_dir=stash.position.y_dir,
        z_dir=stash.position.z_dir,
    )
    new_stash = Stash(
        tier=stash.tier,
        class_name=stash.class_name,
        position=position,
        avg_items_points=stash.avg_items_points,
    )
    db.add(new_stash)
    db.commit()
    db.refresh(new_stash)
    return new_stash


def add_items_to_stash(db: Session, items: List[CreateStashItem]) -> List[StashItem]:
    stash_items = [StashItem(**item.dict()) for item in items]
    db.add_all(stash_items)
    db.commit()
    return stash_items


def get_random_item(items: List[StashItem]) -> StashItem:
    item_chance = [
        i.chance_multiplayer for i in items
    ]
    import random
    return random.choices(items, item_chance)[0]
