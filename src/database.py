import sqlite3
from datetime import datetime, timedelta
from global_config import Config
import schema

from sqlalchemy import create_engine, ForeignKey, String, DateTime, Float, func
from sqlalchemy import select, delete
from sqlalchemy.sql import functions
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


class Base(DeclarativeBase):
    pass


class Purchase(Base):
    __tablename__ = "purchase"
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement="auto", nullable=True)
    name: Mapped[str] = mapped_column(String(50))
    cost: Mapped[float] = mapped_column(Float)
    date: Mapped[datetime] = mapped_column(DateTime)
    category: Mapped[str] = mapped_column(String(50))


class Database:
    def __init__(self, basename: str):
        engine = create_engine(
            f"sqlite:///../{Config.standard_path}/{basename}.db", echo=True)
        self.session = Session(engine)
        Base.metadata.create_all(engine)

    def add_purchase(self, purchase: schema.PurchaseSchemaCreate):
        with self.session as session:
            session.add(Purchase(**purchase.model_dump()))
            session.flush()
            session.commit()

    def delete_purchase(self, purchase_id: int):
        with self.session as session:
            if session.scalar(select(Purchase.id).where(Purchase.id == purchase_id)) == None:
                raise Exception("Object doesn't exist.")
            session.delete(session.get(Purchase, purchase_id))
            session.commit()

    def list_of_purchases(self) -> list[Purchase]:
        with self.session as session:
            return [x[0] for x in session.execute(select(Purchase)).fetchall()]

    def sum_of_purchases(self, category: str) -> float:
        with self.session as session:
            # if
            if category == "all":
                result = session.scalar(functions.sum(Purchase.cost))
            else:
                result = session.query(functions.sum(Purchase.cost)).where(
                    Purchase.category == category).all()

            return result

    def sorted_list_of_purchases(self, sort_by_category: str, by: str) -> list[Purchase]:
        if sort_by_category not in Purchase.__dict__.keys():
            raise Exception("Invalid category name.")
        with self.session as session:
            if by == "asc":
                result = session.execute(
                    select(Purchase).order_by(getattr(Purchase, sort_by_category).asc())).fetchall()
            elif by == "desc":
                result = session.execute(
                    select(Purchase).order_by(getattr(Purchase, sort_by_category).desc())).fetchall()
            else:
                raise Exception("Invalid order.")

            return [x[0] for x in result]

    def get_list_of_purchases_by_date_period(self, period: int) -> list[Purchase]:
        with self.session as session:
            result = session.execute(select(Purchase).filter(
                func.DATE(Purchase.date) >= func.current_date() - timedelta(days=period))).fetchall()
            return [x[0] for x in result]