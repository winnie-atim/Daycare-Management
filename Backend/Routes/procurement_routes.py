from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Models.models import ProcurementItem, Sales
from Connections.connections import get_db
from Schemas.schemas import ProcurementItemCreate, SaleCreate
from typing import List

router = APIRouter()

@router.post("/items")
async def create_procurement_item(item: dict, db: Session = Depends(get_db)):
    db_item = ProcurementItem(**item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/items")
async def read_procurement_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(ProcurementItem).offset(skip).limit(limit).all()
    return items

@router.post("/sales")
async def create_sale(sale: dict, db: Session = Depends(get_db)):
    db_sale = Sales(**sale)
    item = db.query(ProcurementItem).filter(ProcurementItem.id == sale.item_id).first()
    if item:
        if item.quantity < sale.quantity_sold:
            raise HTTPException(status_code=400, detail="Not enough items in stock")
        item.quantity -= sale.quantity_sold
        db.add(db_sale)
        db.commit()
        db.refresh(db_sale)
        return db_sale
    else:
        raise HTTPException(status_code=404, detail="Item not found")
