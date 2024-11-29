from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PurchaseSchemaBase(BaseModel):
    name: str
    cost: float
    date: datetime
    category: str


class PurchaseSchemaCreate(PurchaseSchemaBase):
    pass


class PurchaseSchemaPublic(PurchaseSchemaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
