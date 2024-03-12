from typing import List
from fastapi import APIRouter, Depends
from app.crud.stash import get_stashes, spawn_stash_base, add_items_to_stash, create_stash, get_random_item
from app.dependencies import SessionDep, UserDep
from app.schemas.stash import StashesSchema, PositionSchema, StashItemsSchema, CreateStashItem, CreateStash, \
    StashInfoSchema, StashInfoItemSchema, StashItemSchema

def dep_token(_: UserDep):
    pass


router = APIRouter(
    dependencies=[Depends(dep_token)]
)


@router.get("/", response_model=List[StashesSchema])
def stashes(db: SessionDep):
    stashes = get_stashes(db)
    formated_stashes = []
    for stash in stashes:
        formated_stashes.append(
            StashesSchema(
                id=stash.id,
                position=PositionSchema(
                    x=stash.position.x,
                    y=stash.position.y,
                    z=stash.position.z,
                    x_dir=stash.position.x_dir,
                    y_dir=stash.position.y_dir,
                    z_dir=stash.position.z_dir,
                ),
                tier=stash.tier,
                class_name=stash.class_name,
                avg_items_points=stash.avg_items_points,
            ),
        )

    return formated_stashes


@router.get("/{id}", response_model=StashInfoSchema)
def stash_info(id: int, db: SessionDep):
    stash = spawn_stash_base(db, id)
    return StashInfoSchema(
        id=stash.id,
        tier=stash.tier,
        class_name=stash.class_name,
        position=PositionSchema(
            x=stash.position.x,
            y=stash.position.y,
            z=stash.position.z,
            x_dir=stash.position.x_dir,
            y_dir=stash.position.y_dir,
            z_dir=stash.position.z_dir,
        ),
        avg_items_points=stash.avg_items_points,
        items=[
            StashInfoItemSchema(
                item_id=i.item_id,
                stash_id=i.stash_id,
                points=i.points,
                chance_multiplayer=i.chance_multiplayer,
                class_name=i.item.class_name
            ) for i in stash.items
        ]
    )


@router.get("/spawn/{id}", response_model=StashItemsSchema)
def spawn_items(id: int, player_id: str, db: SessionDep):
    stash = spawn_stash_base(db, id)
    current_item_points = 0
    items_to_spawn = []
    if len(stash.items) > 0:
        while current_item_points < stash.avg_items_points:
            item = get_random_item(stash.items)
            items_to_spawn.append(item)
            current_item_points += item.points
    return StashItemsSchema(
        id=stash.id,
        tier=stash.tier,
        class_name=stash.class_name,
        avg_items_points=stash.avg_items_points,
        items=[
            StashItemSchema(
                item_id=i.item_id,
                class_name=i.item.class_name,
            ) for i in items_to_spawn
        ]
    )


@router.post("/", response_model=StashesSchema)
def post_stash(stash: CreateStash, db: SessionDep):
    stash = create_stash(db, stash)
    return StashesSchema(
        id=stash.id,
        tier=stash.tier,
        class_name=stash.class_name,
        avg_items_points=stash.avg_items_points,
        position=PositionSchema(
            x=stash.position.x,
            y=stash.position.y,
            z=stash.position.z,
            x_dir=stash.position.x_dir,
            y_dir=stash.position.y_dir,
            z_dir=stash.position.z_dir,
        )
    )


@router.post("/items_list", response_model=List[CreateStashItem])
def create_stash_items_list(items_list: List[CreateStashItem], db: SessionDep):
    stashes_res = add_items_to_stash(db, items_list)
    return stashes_res
