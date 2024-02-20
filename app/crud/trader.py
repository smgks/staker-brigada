from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

import app.models as models
from app.schemas import TraderBuyItem

def get_trader_for_player(trader_id: int, player_id: int, db: Session) -> models.Trader | None:
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



