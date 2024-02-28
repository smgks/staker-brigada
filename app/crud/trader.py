from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import aliased

import app.models as models
from app.schemas import TraderBuyItem


def get_trader_spawn(db: Session) -> List[models.Trader]:
    # Create aliases for each item type
    VestItem = aliased(models.Item)
    BackpackItem = aliased(models.Item)
    TopItem = aliased(models.Item)
    BeltItem = aliased(models.Item)
    LegsItem = aliased(models.Item)
    HeadItem = aliased(models.Item)
    FaceItem = aliased(models.Item)
    EyesItem = aliased(models.Item)
    GlovesItem = aliased(models.Item)
    FeetItem = aliased(models.Item)
    ArmbandItem = aliased(models.Item)

    # Query the Trader model with all item joins
    trader = (
        db.query(models.Trader)
        .outerjoin(models.TraderPosition, models.TraderPosition.trader_id == models.Trader.id)
        .outerjoin(models.TraderInventory, models.TraderInventory.trader_id == models.Trader.id)
        # Joining each item type with its respective alias
        .outerjoin(VestItem, models.TraderInventory.vest_id == VestItem.id)
        .outerjoin(BackpackItem, models.TraderInventory.backpack_id == BackpackItem.id)
        .outerjoin(TopItem, models.TraderInventory.top_id == TopItem.id)
        .outerjoin(BeltItem, models.TraderInventory.belt_id == BeltItem.id)
        .outerjoin(LegsItem, models.TraderInventory.legs_id == LegsItem.id)
        .outerjoin(HeadItem, models.TraderInventory.head_id == HeadItem.id)
        .outerjoin(FaceItem, models.TraderInventory.face_id == FaceItem.id)
        .outerjoin(EyesItem, models.TraderInventory.eyes_id == EyesItem.id)
        .outerjoin(GlovesItem, models.TraderInventory.gloves_id == GlovesItem.id)
        .outerjoin(FeetItem, models.TraderInventory.feet_id == FeetItem.id)
        .outerjoin(ArmbandItem, models.TraderInventory.armband_id == ArmbandItem.id)
    )
    return trader.all()


def get_trader_for_player(trader_id: int, player_id: str, db: Session) -> models.Trader | None:
    # add player-specific prices
    trader = db.query(models.Trader).join(
        models.TraderItems
    ).join(
        models.Item
    ).join(
        models.Category
    ).where(
        models.Trader.id == trader_id
    )
    res = db.scalar(trader) 
    return res


def update_item_list_count(
    trader_id: int, 
    player_id: int, 
    items: List[TraderBuyItem], 
    db: Session,
) -> List[models.TraderItems]:
    def ids_from_items(items_l: List[TraderBuyItem]):
        for item in items_l:
            yield item.class_name, item.count

    ids = dict(ids_from_items(items))

    query = db.query(models.TraderItems).join(
        models.Item
    ).where(
        models.Item.class_name.in_(ids.keys())
    ).where(
        models.TraderItems.trader_id == trader_id
    ).where(
        models.TraderItems.count != None
    )
    res = db.scalars(query).all()

    for value in res:
        if value.count is None:
            continue
        if value.count < ids[value.item.class_name]:
            raise HTTPException(400, "Not enough items")
        value.count -= ids[value.item.class_name]
    # commit changes
    db.commit()
    return res


def post_fill_shop(trader_id: int, items: List[TraderBuyItem], db: Session):
    def ids_from_items(items_l: List[TraderBuyItem]):
        for item in items_l:
            yield item.class_name, item.count

    ids = dict(ids_from_items(items))
    query = db.query(models.TraderItems).join(
        models.Item
    ).where(
        models.Item.class_name.in_(ids.keys())
    ).where(
        models.TraderItems.trader_id == trader_id
    ).where(
        models.TraderItems.count != None
    )
    res = db.scalars(query).all()
    for value in res:
        if value.count is None:
            continue
        value.count += ids[value.item.class_name]
    db.commit()
    return res



