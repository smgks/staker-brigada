from pydantic import BaseModel, ConfigDict


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
