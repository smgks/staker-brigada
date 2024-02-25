from enum import unique
from operator import index
from os import name
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, ForeignKeyConstraint, UniqueConstraint
from typing import List, Optional

from starlette.routing import request_response

from app.db import Base
from app.schemas import items


class Category(Base):
    __tablename__ = "category"
    __table_args__ = {"schema": "game"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)
    items: Mapped[List["Item"]] = relationship(back_populates="category")


class Trader(Base):
    __tablename__ = "trader"
    __table_args__ = {"schema": "game"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)
    items: Mapped[List["TraderItems"]] = relationship()
    position: Mapped[Optional["TraderPosition"]] = relationship("TraderPosition", uselist=False, back_populates="trader")
    inventory: Mapped[Optional["TraderInventory"]] = relationship("TraderInventory", uselist=False, back_populates="trader")


class TraderPosition(Base):
    __tablename__ = "trader_position"
    __table_args__ = {"schema": "game"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    trader_id: Mapped[int] = mapped_column(ForeignKey("game.trader.id", ondelete="CASCADE"), index=True)
    x: Mapped[float] = mapped_column()
    y: Mapped[float] = mapped_column()
    z: Mapped[float] = mapped_column()
    trader: Mapped[Trader] = relationship("Trader", back_populates="position")
    x_dir: Mapped[float] = mapped_column()
    y_dir: Mapped[float] = mapped_column()
    z_dir: Mapped[float] = mapped_column()


class TraderInventory(Base):
    __tablename__ = "trader_inventory"
    __table_args__ = {"schema": "game"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    trader_id: Mapped[int] = mapped_column(ForeignKey("game.trader.id", ondelete="CASCADE"), index=True)
    skin_name: Mapped[str] = mapped_column()
    vest_id: Mapped[int | None] = mapped_column(ForeignKey("game.items.id", ondelete="SET NULL"))
    vest: Mapped["Item"] = relationship("Item", foreign_keys=[vest_id])
    backpack_id: Mapped[int | None] = mapped_column(ForeignKey("game.items.id", ondelete="SET NULL"))
    backpack: Mapped["Item"] = relationship("Item", foreign_keys=[backpack_id])
    top_id: Mapped[int | None] = mapped_column(ForeignKey("game.items.id", ondelete="SET NULL"))
    top: Mapped["Item"] = relationship("Item", foreign_keys=[top_id])
    belt_id: Mapped[int | None] = mapped_column(ForeignKey("game.items.id", ondelete="SET NULL"))
    belt: Mapped["Item"] = relationship("Item", foreign_keys=[belt_id])
    legs_id: Mapped[int | None] = mapped_column(ForeignKey("game.items.id", ondelete="SET NULL"))
    legs: Mapped["Item"] = relationship("Item", foreign_keys=[legs_id])
    head_id: Mapped[int | None] = mapped_column(ForeignKey("game.items.id", ondelete="SET NULL"))
    head: Mapped["Item"] = relationship("Item", foreign_keys=[head_id])
    face_id: Mapped[int | None] = mapped_column(ForeignKey("game.items.id", ondelete="SET NULL"))
    face: Mapped["Item"] = relationship("Item", foreign_keys=[face_id])
    eyes_id: Mapped[int | None] = mapped_column(ForeignKey("game.items.id", ondelete="SET NULL"))
    eyes: Mapped["Item"] = relationship("Item", foreign_keys=[eyes_id])
    gloves_id: Mapped[int | None] = mapped_column(ForeignKey("game.items.id", ondelete="SET NULL"))
    gloves: Mapped["Item"] = relationship("Item", foreign_keys=[gloves_id])
    feet_id: Mapped[int | None] = mapped_column(ForeignKey("game.items.id", ondelete="SET NULL"))
    feet: Mapped["Item"] = relationship("Item", foreign_keys=[feet_id])
    armband_id: Mapped[int | None] = mapped_column(ForeignKey("game.items.id", ondelete="SET NULL"))
    armband: Mapped["Item"] = relationship("Item", foreign_keys=[armband_id])
    trader: Mapped[Trader] = relationship("Trader", back_populates="inventory")



class TraderItems(Base):
    __tablename__ = "trader_items"
    __table_args__ = {"schema": "game"}

    trader_id: Mapped[int] = mapped_column(ForeignKey("game.trader.id", ondelete="CASCADE"), primary_key=True,
                                           index=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("game.items.id", ondelete="CASCADE"), primary_key=True, index=True)
    price: Mapped[int | None] = mapped_column()
    sell_price: Mapped[int | None] = mapped_column()
    count: Mapped[int | None] = mapped_column()
    item: Mapped["Item"] = relationship()
    points: Mapped[Optional["TraderItemsPoints"]] = relationship(
        "TraderItemsPoints",
        back_populates="trader_item"
    )


class TraderItemsPoints(Base):
    __tablename__ = "trader_items_points"
    __table_args__ = (
        ForeignKeyConstraint(
            ['trader_id', 'item_id'], ['game.trader_items.trader_id', 'game.trader_items.item_id'],
            ondelete="CASCADE"
        ),
        {"schema": "game"},
    )

    trader_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    item_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    points: Mapped[int] = mapped_column()
    required_points: Mapped[int] = mapped_column()
    trader_item: Mapped["TraderItems"] = relationship("TraderItems", back_populates="points")


class Item(Base):
    __tablename__ = "items"
    __table_args__ = {"schema": "game"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    class_name: Mapped[str] = mapped_column(unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("game.category.id", ondelete="CASCADE"))
    category: Mapped["Category"] = relationship(back_populates="items")


class Faction(Base):
    __tablename__ = "factions"
    __table_args__ = {"schema": "game"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column()
    players: Mapped[List["Player"]] = relationship(back_populates="faction")


class Player(Base):
    __tablename__ = "players"
    __table_args__ = {"schema": "game"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column()
    faction_id: Mapped[int] = mapped_column(ForeignKey("game.factions.id", ondelete="CASCADE"))
    faction: Mapped[Faction] = relationship(Faction, back_populates="players")
    level: Mapped[int] = mapped_column(default=1)


class Bank(Base):
    __tablename__ = "bank"
    __table_args__ = {"schema": "game"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    commission: Mapped[int] = mapped_column()
    max_money: Mapped[int] = mapped_column()
    deposits: Mapped[List["BankDeposit"]] = relationship("BankDeposit", back_populates="bank")


class BankDeposit(Base):
    __tablename__ = "bank_deposit"
    __table_args__ = {"schema": "game"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("game.players.id", ondelete="CASCADE"))
    money: Mapped[int] = mapped_column()
    bank_id: Mapped[int] = mapped_column(ForeignKey("game.bank.id", ondelete="CASCADE"))
    bank: Mapped[Bank] = relationship("Bank", back_populates="deposits")
