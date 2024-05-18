from Models.models import Sitter, DailyPayment, PresentSitter
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, date
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
    

def present_sitter(db: Session, sitter_id: int):
    print(f"Presenting sitter with id: {sitter_id}")
    try:
        new_present = PresentSitter(sitter_id=sitter_id, date=datetime.now())
        Sitter.update_sitter_status(db, sitter_id)
        db.add(new_present)
        db.commit()
        return {
            "message": "Sitter marked present",
            "status_code": 200
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
def new_day_sitter(db: Session, sitter_id: int):
    print(f"Defaulting status for sitter with id: {sitter_id}")
    try:
        Sitter.update_sitter_status_on_new_day(db, sitter_id)
        return {
            "message": "Sitter status updated to default",
            "status_code": 200
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
def get_all_present_sitters(db: Session):
    print("Getting all present sitters")
    try:
        present_sitters = (db.query(PresentSitter).options(joinedload(PresentSitter.sitter)).all())
        return {"data": present_sitters}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

def get_sitters_bill(db: Session):
    print("Getting all sitters bill")
    try:
        sitters = (db.query(DailyPayment).options(joinedload(DailyPayment.sitter)).all())
        print(sitters)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

def update_when_paid(db: Session, sitter_id: int):
    try:
        sitter = db.query(DailyPayment).filter_by(sitter_id=sitter_id).first()
        if sitter:
            sitter.is_paid = True
            sitter.payment_date = datetime.now()
            db.commit()
            return {
                "message": "Payment updated successfully",
                "status_code": 200
            }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
def get_all_sitters(db: Session):
    print("Getting all sitters")
    try:
        sitters = db.query(Sitter).all()
        return {"data": sitters}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
def create_daily_payment_for_all_sitters(db: Session):
    sitters = db.query(Sitter).all()
    for sitter in sitters:
        new_payment = DailyPayment(
            sitter_id=sitter.id,
            date=datetime.now()
        )
        db.add(new_payment)
    db.commit()

def get_unpaid_sitters_bill(db: Session):
    try:
        today = date.today()
        sitters = (db.query(DailyPayment)
                   .filter(DailyPayment.is_paid == False, DailyPayment.date >= today)
                   .options(joinedload(DailyPayment.sitter))
                   .all())
        return sitters
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

def update_payment_status(db: Session, sitter_id: int):
    try:
        sitter_payment = db.query(DailyPayment).filter_by(sitter_id=sitter_id, is_paid=False).first()
        if sitter_payment:
            sitter_payment.is_paid = True
            sitter_payment.payment_date = datetime.now()
            db.commit()
            return {
                "message": "Payment updated successfully",
                "status_code": 200
            }
        else:
            raise HTTPException(status_code=404, detail="Sitter payment record not found or already paid")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")