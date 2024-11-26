import database
from dtclasses import Purchase, Income


class Repository:
    def __init__(self, basename: str):
        self.__db = database.Database(basename)

    def add_purchase(self, purchase: Purchase):
        self.__db.add_purchase(purchase)

    def delete_purchase(self, purchase: Purchase):
        self.__db.delete_purchase(purchase)
