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


class TraderItems(Base):
    __tablename__ = "trader_items"
    __table_args__ = {"schema": "game"}

    trader_id: Mapped[int] = mapped_column(ForeignKey("game.trader.id", ondelete="CASCADE"), primary_key=True, index=True)
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
            ['trader_id', 'item_id'],['game.trader_items.trader_id', 'game.trader_items.item_id'],
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
