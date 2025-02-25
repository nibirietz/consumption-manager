from database import Database
from datetime import datetime
from fastapi import FastAPI
import schema

app = FastAPI()
db = Database("test")


@app.get("/")
def root():
    return {"message": "Start Server!"}


@app.get("/purchases")
def get_purchases():
    purchases = [schema.PurchaseSchemaPublic.model_validate(
        x) for x in db.list_of_purchases()]
    output = [x.model_dump() for x in purchases]
    print(output)
    return output


@app.post("/create_purchase", response_model=schema.PurchaseSchemaCreate)
def create_purchase(purchase: schema.PurchaseSchemaCreate):
    print(purchase)
    db.add_purchase(purchase)
    return purchase


@app.delete("/delete_purchase/{id}")
def delete_purchase(purchase_id: int):
    db.delete_purchase(purchase_id)


@app.get("/sum_of_purchases/{category}")
def get_sum_of_purchases(category: str = "all"):
    return db.sum_of_purchases(category=category)


@app.get("/sorted_list_of_purchases/{category}/{by}")
def sorted_list_of_purchases(category: str, by: str):
    purchases = [schema.PurchaseSchemaPublic.model_validate(
        x) for x in db.sorted_list_of_purchases(sort_by_category=category, by=by)]
    output = [x.model_dump() for x in purchases]
    print(output)
    return output


@app.get("/period_of_purchases")
def get_period_of_purchases(period: int = 7):
    purchases = [schema.PurchaseSchemaPublic.model_validate(
        x) for x in db.get_list_of_purchases_by_date_period(period)]
    print(purchases)
    output = [x.model_dump() for x in purchases]
    print(output)
    return output
