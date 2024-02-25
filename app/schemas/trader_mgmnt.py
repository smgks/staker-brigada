from pydantic import BaseModel, ConfigDict


class TraderCreateInventoryItems(BaseModel):
    skin_name: str
    vest_id: int | None
    backpack_id: int | None
    top_id: int | None
    belt_id: int | None
    legs_id: int | None
    head_id: int | None
    face_id: int | None
    eyes_id: int | None
    gloves_id: int | None
    feet_id: int | None
    armband_id: int | None

    model_config = ConfigDict(from_attributes=True)


class TraderCreateSpawnPosition(BaseModel):
    x: float
    y: float
    z: float
    x_dir: float
    y_dir: float
    z_dir: float

    model_config = ConfigDict(from_attributes=True)


class UpdateTrader(BaseModel):
    name: str | None


class FullUpdateTraderItemPoints(BaseModel):
    points: int
    required_points: int


class FullUpdateTraderItem(BaseModel):
    price: int | None
    sell_price: int | None
    count: int | None
    points: FullUpdateTraderItemPoints | None


class NewTrader(BaseModel):
    name: str
    inventory: TraderCreateInventoryItems | None
    pos: TraderCreateSpawnPosition | None


class CreatedTrader(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class NewTraderItemPoints(BaseModel):
    points: int
    required_points: int


class NewTraderItem(BaseModel):
    item_id: int
    price: int | None
    sell_price: int | None
    count: int | None
    points: NewTraderItemPoints | None
