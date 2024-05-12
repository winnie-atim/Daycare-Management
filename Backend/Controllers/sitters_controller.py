from Models.models import Sitter, DailyPayment
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
async def create_sitter(db_session: Session, sitter: dict):
    try:
        new_sitter = Sitter.create_sitter(db_session, sitter)
        adding_siter_payment(db_session, new_sitter.id)
        return {
             "sitter_id": new_sitter.id,
            "name": new_sitter.name,
            "location": new_sitter.location,
        }
    
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
def adding_siter_payment(db: Session, sitter_id: int):
    try:
        new_payment = DailyPayment(sitter_id=sitter_id)
        db.add(new_payment)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
def update_baby_number(db: Session, sitter_id: int):
    try:
        sitter = db.query(DailyPayment).filter_by(sitter_id=sitter_id).first()
        if sitter:
            sitter.number_of_babies += 1
            sitter.total_amount = sitter.number_of_babies * sitter.amount
            db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

def paysitter(db: Session, sitter_id: int):
    try:
        sitter = db.query(DailyPayment).filter_by(sitter_id=sitter_id).first()
        if sitter:
            sitter.payment_date = datetime.now()
            sitter.is_paid = True
            db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")