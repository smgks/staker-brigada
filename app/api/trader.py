from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.schemas import TraderShop, TraderBuyItem, TraderItem, TraderCategory, TraderSpawn, TraderInventoryItems, \
    TraderSpawnPosition, SimpleItem
from app.crud import get_trader_for_player, post_fill_shop, update_item_list_count, get_trader_spawn
from app.dependencies import UserDep, SessionDep


def tocken_dep(token: UserDep):
    pass


router = APIRouter(
    dependencies=[Depends(tocken_dep)]
)


@router.get("/spawn", response_model=List[TraderSpawn])
def spawn_traders(db: SessionDep):
    traders = get_trader_spawn(db)
    res = []
    for trader in traders:
        if trader is None:
            raise HTTPException(status_code=404, detail="Trader not found")
        res.append(
            TraderSpawn(
                id=trader.id,
                name=trader.name,
                pos=TraderSpawnPosition(
                    id=trader.position.id,
                    x=trader.position.x,
                    y=trader.position.y,
                    z=trader.position.z,
                    x_dir=trader.position.x_dir,
                    y_dir=trader.position.y_dir,
                    z_dir=trader.position.z_dir,
                ) if trader.position is not None else None,
                items=TraderInventoryItems(
                    id=trader.inventory.id,
                    skin_name=trader.inventory.skin_name,
                    vest=SimpleItem(
                        id=trader.inventory.vest_id,
                        class_name=trader.inventory.vest.class_name
                    ) if trader.inventory.vest_id is not None else None,
                    backpack=SimpleItem(
                        id=trader.inventory.backpack_id,
                        class_name=trader.inventory.backpack.class_name
                    ) if trader.inventory.backpack_id is not None else None,
                    top=SimpleItem(
                        id=trader.inventory.top_id,
                        class_name=trader.inventory.top.class_name
                    ) if trader.inventory.top_id is not None else None,
                    belt=SimpleItem(
                        id=trader.inventory.belt_id,
                        class_name=trader.inventory.belt.class_name
                    ) if trader.inventory.belt_id is not None else None,
                    legs=SimpleItem(
                        id=trader.inventory.legs_id,
                        class_name=trader.inventory.legs.class_name
                    ) if trader.inventory.legs_id is not None else None,
                    head=SimpleItem(
                        id=trader.inventory.head_id,
                        class_name=trader.inventory.head.class_name
                    ) if trader.inventory.head_id is not None else None,
                    face=SimpleItem(
                        id=trader.inventory.face_id,
                        class_name=trader.inventory.face.class_name
                    ) if trader.inventory.face_id is not None else None,
                    eyes=SimpleItem(
                        id=trader.inventory.eyes_id,
                        class_name=trader.inventory.eyes.class_name
                    ) if trader.inventory.eyes_id is not None else None,
                    gloves=SimpleItem(
                        id=trader.inventory.gloves_id,
                        class_name=trader.inventory.gloves.class_name
                    ) if trader.inventory.gloves_id is not None else None,
                    feet=SimpleItem(
                        id=trader.inventory.feet_id,
                        class_name=trader.inventory.feet.class_name
                    ) if trader.inventory.feet_id is not None else None,
                    armband=SimpleItem(
                        id=trader.inventory.armband_id,
                        class_name=trader.inventory.armband.class_name
                    ) if trader.inventory.armband_id is not None else None,
                ) if trader.inventory is not None else None,
            )
        )
    return res


@router.get("/items/{trader_id}/{player_id}", response_model=TraderShop)
def get_trader(trader_id: int, player_id: str, db: SessionDep):
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
        id=trader_id,
        steamid=player_id,
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

