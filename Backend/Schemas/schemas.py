from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProcurementItemCreate(BaseModel):
    name: str
    category: str
    quantity: int
    price: float

class ProcurementItem(BaseModel):
    id: int
    name: str
    category: str
    quantity: int
    price: float
    date_added: datetime

    class Config:
        orm_mode = True

class SaleCreate(BaseModel):
    item_id: int
    quantity_sold: int
    total_amount: float

class Sales(BaseModel):
    id: int
    item_id: int
    quantity_sold: int
    sale_date: datetime
    total_amount: float

    class Config:
        orm_mode = True
