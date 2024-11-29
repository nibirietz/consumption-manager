from database import Database
from datetime import datetime
from fastapi import FastAPI
import schema

app = FastAPI()
db = Database("test")


@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.get("/purchases/")
def get_purchases():
    purchases = [schema.PurchaseSchemaPublic.model_validate(
        x) for x in db.list_of_purchases()]
    print(purchases)
    return [x.model_dump() for x in purchases]


@app.post("/purchases/", response_model=schema.PurchaseSchemaCreate)
def create_purchase(purchase: schema.PurchaseSchemaCreate):
    print(purchase)
    db.add_purchase(purchase)
    return purchase
