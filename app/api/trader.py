from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.schemas import TraderShop, TraderBuyItem, TraderItem, TraderCategory
from app.crud import get_trader_for_player, post_fill_shop, update_item_list_count
from app.dependencies import UserDep, SessionDep

def tocken_dep(token: UserDep):
    pass

router = APIRouter(
    dependencies=[Depends(tocken_dep)]
)


@router.get("/items/{trader_id}/{player_id}", response_model=TraderShop)
def get_trader(trader_id: int, player_id: int, db: SessionDep):
    trader = get_trader_for_player(trader_id, player_id, db)
    if trader is None:
        raise HTTPException(status_code=404, detail="Trader not found or unavalible for current user")
    categories = dict()
    for trader_item in trader.items:
        cat = trader_item.item.category
        if categories.get(cat.name, None) is None:
            categories[cat.name] = TraderCategory(
                category_name=cat.name,
                items=[
                    TraderItem(
                        id=trader_item.item_id,
                        price=trader_item.price,
                        sell_price=trader_item.sell_price,
                        count=trader_item.count,
                        class_name=trader_item.item.class_name
                    )
                ]
            )
        else:
            categories[cat.name].items.append(
                TraderItem(
                    id=trader_item.item_id,
                    price=trader_item.price,
                    sell_price=trader_item.sell_price,
                    count=trader_item.count,
                    class_name=trader_item.item.class_name
                )
            )
    return TraderShop(
        name=trader.name,
        categories=[v for k, v in categories.items()]
    )


@router.post("/buy_items/{trader_id}/{player_id}")
async def buy_items(trader_id: int, player_id: int, items: List[TraderBuyItem], db: SessionDep):
    items_l = update_item_list_count(trader_id, player_id, items, db)
    return [
        TraderItem(
            id=i.item_id,
            price=i.price,
            sell_price=i.sell_price,
            count=i.count,
            class_name=i.item.class_name
        ) for i in items_l
    ]

