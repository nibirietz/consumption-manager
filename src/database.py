import sqlite3
from datetime import datetime
from global_config import config
from dtclasses import Purchase

from sqlalchemy import create_engine, ForeignKey, String, DateTime, Float
from sqlalchemy import select, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


class Base(DeclarativeBase):
    pass


class PurchaseTable(Base):
    __tablename__ = "purchase"
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement="auto", nullable=True)
    name: Mapped[str] = mapped_column(String(50))
    cost: Mapped[float] = mapped_column(Float)
    date: Mapped[datetime] = mapped_column(DateTime)

    def __init__(self, name: str, cost: float, date: datetime):
        self.name = name
        self.cost = cost
        self.date = date


class Database:
    def __init__(self, basename: str):
        engine = create_engine(
            f"sqlite:///{config["path"]}/{basename}.db", echo=True)
        print(engine)
        self.session = Session(engine)
        Base.metadata.create_all(engine)

    def __convert_dataclass_to_table(self, purchase: Purchase):
        return PurchaseTable(name=purchase.name, cost=purchase.cost, date=purchase.date)

    def add_purchase(self, purchase: Purchase):
        purchase_sql = self.__convert_dataclass_to_table(purchase)
        with self.session as session:
            session.add(purchase_sql)
            session.flush()
            session.commit()

    def delete_purchase(self, purchase: Purchase):
        purchase_sql = self.__convert_dataclass_to_table(purchase)
        print(purchase_sql.id)
        with self.session as session:
            # stmt = delete(PurchaseTable).where(
            # PurchaseTable.c.date == purchase_sql.date)
            # session.delete(session.query(PurchaseTable).get(purchase_sql.date))
            session.commit()
