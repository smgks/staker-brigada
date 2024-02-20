from typing import List
from fastapi import APIRouter, Depends
from app.crud import create_trader, get_trader_tems_points, get_traders, remove_trader
from app.crud.trader_mgmnt import create_trader_items, full_update_trader_item, remove_trader_items, update_trader

from app.dependencies import SessionDep, UserDep
from app.crud import post_fill_shop
from app.schemas import TraderItem, TraderBuyItem
from app.schemas.trader_mgmnt import CreatedTrader, FullUpdateTraderItem, NewTrader, NewTraderItem, NewTraderItemPoints, UpdateTrader


def dep_token(_: UserDep):
    pass


router = APIRouter(
    dependencies=[Depends(dep_token)]
)


@router.post("/add_supply/{trader_id}")
def supply_trader(trader_id: int, items: List[TraderBuyItem], db: SessionDep):
    items_l = post_fill_shop(trader_id, items, db)
    return [
        TraderItem(
            id=i.item_id,
            price=i.price,
            sell_price=i.sell_price,
            count=i.count,
            class_name=i.item.class_name
        ) for i in items_l
    ]

@router.get("/trader", response_model= List[CreatedTrader])
def trader_list(
    db: SessionDep,
):
    return get_traders(db)

@router.post("/trader", response_model=CreatedTrader)
def post_trader(
    db: SessionDep,
    trader: NewTrader
):
    return create_trader(
        db,
        trader,
    )


@router.get("/trader/{trader_id}/items", response_model=List[NewTraderItem])
def trader_items(
    db: SessionDep,
    trader_id: int,
):
    trader_items = get_trader_tems_points(db, trader_id)
    return [
        NewTraderItem(
            item_id=i.item_id,
            price=i.price,
            sell_price=i.sell_price,
            count=i.count,
            points=None if i.points is None else NewTraderItemPoints(points=i.points.points, required_points=i.points.required_points),
        ) for i in trader_items
    ]

@router.delete("/trader/{trader_id}")
def delete_trader(
    db: SessionDep,
    trader_id: int,
):
    return remove_trader(db, trader_id)



@router.post("/trader/{trader_id}/items", response_model=List[NewTraderItem])
def post_trader_items(
    db: SessionDep,
    trader_id: int,
    items: List[NewTraderItem]
):
    _items = create_trader_items(db, trader_id, items)   
    return [
        NewTraderItem(
            item_id=i.item_id,
            price=i.price,
            sell_price=i.sell_price,
            count=i.count,
            points=None if i.points is None else NewTraderItemPoints(points=i.points.points, required_points=i.points.required_points),
        ) for i in _items
    ]


@router.delete("/trader/{trader_id}/items")
def delete_trader_items(
    db: SessionDep,
    trader_id: int,
    items: List[int],
):
    remove_trader_items(db, trader_id, items)
    

@router.post("/trader/{trader_id}", response_model=UpdateTrader)
def trader_update(
    db: SessionDep,
    trader_id: int,
    data: UpdateTrader,
):
    return update_trader(db, trader_id, data)


@router.post("/trader/{trader_id}/items/{item_id}", response_model=FullUpdateTraderItem)
def trader_items_full_update(
    db: SessionDep,
    trader_id: int,
    item_id: int,
    data: FullUpdateTraderItem,
):
    return full_update_trader_item(db, trader_id, item_id, data)

