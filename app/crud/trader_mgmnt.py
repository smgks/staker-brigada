from typing import List
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_
from sqlalchemy.sql.coercions import expect
from app.errors.errors import ItemNotFound, UniqueConstraintException

from app.models import Trader, TraderItems, TraderItemsPoints
from app.schemas import NewTraderItem, CreatedTrader, NewTrader, NewTraderItemPoints
from app.schemas.trader_mgmnt import FullUpdateTraderItem, UpdateTrader

def get_traders(
    db: Session
) -> List[Trader]:
    return db.query(
        Trader
    ).all()

def remove_trader(
    db: Session,
    trader_id: int,
) -> int:
    res = db.query(Trader).where(Trader.id == trader_id).delete()
    db.commit()
    return res

def create_trader(
    db: Session,
    trader: NewTrader,
) -> Trader:
    _trader = Trader(
        name=trader.name,
    )
    db.add(_trader)
    db.commit()
    db.refresh(_trader)
    return _trader

def create_trader_items(
    db: Session,
    trader_id: int,
    items: List[NewTraderItem]
) -> List[TraderItems]:
    _items = [
        TraderItems(
            price=i.price,
            sell_price=i.sell_price,
            count=i.count,
            trader_id=trader_id,
            item_id=i.item_id,
            points=TraderItemsPoints(
                trader_id=trader_id,
                item_id=i.item_id,
                points=i.points.points,
                required_points=i.points.required_points,
            ) if i.points is not None else None
        ) for i in items
    ]
    try:
        db.add_all(_items)
        db.commit()
    except IntegrityError:
        raise UniqueConstraintException()
    return _items


def get_trader_items(
    db: Session,
    trader_id: int,
) -> List[TraderItems]:
    return db.query(TraderItems).where(TraderItems.trader_id == trader_id).all()


def get_trader_tems_points(
    db: Session,
    trader_id: int,
) -> List[TraderItems]:
    return db.query(TraderItems).outerjoin(TraderItemsPoints, and_(
        TraderItems.trader_id == TraderItemsPoints.trader_id,
        TraderItems.item_id == TraderItemsPoints.item_id),
    ).where(TraderItems.trader_id == trader_id).all()


def remove_trader_items(
    db: Session,
    trader_id: int,
    ids: List[int],
) -> int:
    res = db.query(TraderItems).where(TraderItems.item_id.in_(ids)).where(TraderItems.trader_id == trader_id).delete()
    db.commit()
    return res


def update_trader(
    db: Session,
    trader_id: int,
    data: UpdateTrader
):
    _data = db.query(Trader).get(trader_id)
    if _data is None:
        raise ItemNotFound()
    to_update = data.model_dump(exclude_unset=True)
    
    for key, value in to_update.items():
        setattr(_data, key, value)
    db.commit()
    db.refresh(_data)
    return _data


def full_update_trader_item(
    db: Session,
    trader_id: int,
    item_id: int,
    data: FullUpdateTraderItem,
):
    _data = db.query(TraderItems).outerjoin(TraderItemsPoints, and_(
        TraderItems.trader_id == TraderItemsPoints.trader_id,
        TraderItems.item_id == TraderItemsPoints.item_id),
    ).where(
        TraderItems.trader_id == trader_id
    ).where(
        TraderItems.item_id == item_id
    ).first()
    
    if _data is None:
        raise ItemNotFound()

    to_update = data.model_dump(
        exclude={"points"},
    )

    for key, value in to_update.items():
        setattr(_data, key, value)
    
    if (data.points is None and _data.points is not None):
        db.delete(_data.points)
        _data = None
    elif data.points is not None:
        if _data.points is not None:
            db.delete(_data.points)
        _data.points = TraderItemsPoints(
            trader_id=trader_id,
            item_id=item_id,
            points=data.points.points,
            required_points=data.points.required_points,
        )

    db.commit()
    db.refresh(_data)
    return _data
