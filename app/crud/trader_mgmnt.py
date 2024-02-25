from typing import List
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_
from sqlalchemy.sql.coercions import expect
from app.errors.errors import ItemNotFound, UniqueConstraintException

from app.models import Trader, TraderItems, TraderItemsPoints, TraderPosition, TraderInventory
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
    inventory = TraderInventory(
        skin_name=trader.inventory.skin_name,
        vest_id=trader.inventory.vest_id,
        backpack_id=trader.inventory.backpack_id,
        top_id=trader.inventory.top_id,
        belt_id=trader.inventory.belt_id,
        legs_id=trader.inventory.legs_id,
        head_id=trader.inventory.head_id,
        face_id=trader.inventory.face_id,
        eyes_id=trader.inventory.eyes_id,
        gloves_id=trader.inventory.gloves_id,
        feet_id=trader.inventory.feet_id,
        armband_id=trader.inventory.armband_id,
    ) if trader.inventory is not None else None
    positions = TraderPosition(
        x=trader.pos.x,
        y=trader.pos.y,
        z=trader.pos.z,
        x_dir=trader.pos.x_dir,
        y_dir=trader.pos.y_dir,
        z_dir=trader.pos.z_dir,
    ) if trader.pos is not None else None
    _trader = Trader(
        name=trader.name,
        position=positions,
        inventory=inventory
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
    data: NewTrader
):
    _data = db.query(
        Trader
    ).outerjoin(
        TraderPosition
    ).outerjoin(
        TraderInventory
    ).where(
        Trader.id == trader_id
    )
    _data = db.scalar(_data)

    if _data is None:
        raise ItemNotFound()

    _data.name = data.name
    if data.pos is not None:
        if _data.position is not None:
            for key, value in data.pos.dict().items():
                setattr(_data.position, key, value)
        else:
            _data.position = TraderPosition(
                x=data.pos.x,
                y=data.pos.y,
                z=data.pos.z,
                x_dir=data.pos.x_dir,
                y_dir=data.pos.y_dir,
                z_dir=data.pos.z_dir,
            )
    if data.inventory is not None:
        if _data.inventory is not None:
            for key, value in data.inventory.dict().items():
                setattr(_data.inventory, key, value)
        else:
            _data.inventory = TraderInventory(
                skin_name=data.inventory.skin_name,
                vest_id=data.inventory.vest_id,
                backpack_id=data.inventory.backpack_id,
                top_id=data.inventory.top_id,
                belt_id=data.inventory.belt_id,
                legs_id=data.inventory.legs_id,
                head_id=data.inventory.head_id,
                face_id=data.inventory.face_id,
                eyes_id=data.inventory.eyes_id,
                gloves_id=data.inventory.gloves_id,
                feet_id=data.inventory.feet_id,
                armband_id=data.inventory.armband_id,
            )

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

