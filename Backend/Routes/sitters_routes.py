from fastapi import APIRouter, HTTPException, Depends
from Connections.connections import get_db
from sqlalchemy.orm import Session

from Controllers.sitters_controller import (
    create_sitter,
    present_sitter,
    get_all_present_sitters,
    update_when_paid,
    get_all_sitters,
    get_unpaid_sitters_bill,
    get_sitters_bill,
    new_day_sitter,
    update_payment_status,
    create_daily_payment_for_all_sitters
)

router = APIRouter()

@router.get("/")
async def read_root():
    return {"Sitters" : "Hello World"}

@router.post("/create_sitter")
async def create_sitter_route(sitter: dict, db: Session = Depends(get_db)):
    try:
        created_sitted =  await create_sitter(db, sitter)
        if created_sitted:
            return {"message": "Sitter created successfully", "status": 200, "data": created_sitted}
        else:
            raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
@router.get("/get_all_sitters")
async def get_all_sitters_route(db: Session = Depends(get_db)):
    try:
        sitters = get_all_sitters(db)
        if sitters:
            return sitters
        else:
            raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
@router.post("/present_sitter/")
async def present_sitter_route(sitter_id: int, db: Session = Depends(get_db)):
    try:
        present = present_sitter(db, sitter_id)
        if present:
            return present
        else:
            raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
@router.put("/new_day_sitter/")
async def present_new_day_sitter(sitter_id: int, db: Session = Depends(get_db)):
    try:
        present = new_day_sitter(db, sitter_id)
        if present:
            return present
        else:
            raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
@router.get("/get_all_present_sitters")
async def get_all_present_sitters_route(db: Session = Depends(get_db)):
    try:
        present_sitters = get_all_present_sitters(db)
        if present_sitters:
            return present_sitters
        else:
            raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router.get("/get_all_sitters_bill")
async def get_all_sitters_bill_route(db: Session = Depends(get_db)):
    try:
        sitters = get_unpaid_sitters_bill(db)
        if sitters:
            return sitters
        else:
            raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
@router.put("/update_payment/")
async def update_payment_route(sitter_id: int, db: Session = Depends(get_db)):
    try:
        updated_payment = update_payment_status(db, sitter_id)
        return updated_payment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
@router.post("/reset_daily_payments")
async def reset_daily_payments_route(db: Session = Depends(get_db)):
    try:
        create_daily_payment_for_all_sitters(db)
        return {"message": "Daily payments reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
