from Models.models import Baby, BabyRelease, PresentBaby
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session, joinedload
from Controllers.sitters_controller import update_baby_number
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Any

def automate_by_fee(new_baby):
    if new_baby.fee == 15000:
        new_baby.duration = 'full_day'
        new_baby.payment_type = 'daily'
    elif new_baby.fee == 10000:
        new_baby.duration = 'half_day'
        new_baby.payment_type = 'daily'
    else:
        new_baby.is_monthly = True
        new_baby.payment_type = 'monthly'
        new_baby.duration = 'full_day'

def create_baby_controller(db: Session, baby_data: dict):
    print("""Creating baby""")
    try:
        new_baby = Baby(**baby_data) 
        new_baby.baby_access = generate_access_number(db)
        update_baby_number(db, new_baby.sitter_assigned)
        automate_by_fee(new_baby)
        
        db.add(new_baby)
        db.commit()
        db.refresh(new_baby)
        return {
            "message": "Baby created successfully",
            "status_code": 200,
            "data": new_baby
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
def generate_access_number(db: Session):
    print("""Generating Baby Access """)
    last_baby = db.query(Baby).order_by(Baby.id.desc()).first()
    if last_baby.baby_access is None:
        return "A00001"
    else:
        letter, number_str = last_baby.baby_access[0], last_baby.baby_access[1:]
        number = int(number_str) + 1
        if number > 99999:
            letter = chr(ord(letter) + 1) 
            number = 1

        return f"{letter}{number:05d}"
        
def update_baby(db: Session,baby_data):
    print("""Updating baby""")
    baby_access = baby_data['baby_access']
    baby = db.query(Baby).filter_by(baby_access=baby_access).first()

    if baby:
        baby.name_of_brought_person = baby_data['name_of_brought_person']
        baby.time_of_arrival = baby_data['time_of_arrival']
        baby.fee = baby_data['fee']
        baby.sitter_assigned = baby_data['sitter_assigned']
        update_baby_number(db, baby.sitter_assigned)
        automate_by_fee(baby)

        db.commit()
        return baby
    
def relaese_baby(db: Session, baby_data):
    print("""Releasing baby""")
    try:
        release = BabyRelease(**baby_data)
        db.add(release)
        db.commit()

        return {
            "message": "Baby released successfully",
            "status_code": 200,
            "data": release
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
def get_all_babies(db: Session):
    print("""Getting all babies""")
    babies = db.query(Baby).all()
    if babies:
        return {
            "message": "Babies retrieved successfully",
            "status_code": 200,
            "data": {"data": babies}
        }
    else:
        raise HTTPException(status_code=400, detail="An error occurred")
    
def get_baby_by_access(db: Session, baby_access: str):
    print(f"""Getting baby with access: {baby_access}""")
    baby = db.query(Baby).filter_by(baby_access=baby_access).first()
    if baby:
        return {
            "message": "Baby retrieved successfully",
            "status_code": 200,
            "data": baby
        }
    else:
        raise HTTPException(status_code=400, detail="An error occurred")
    
def add_baby_to_present(db: Session, baby_id: int):
    print("""Adding baby to present""")
    try:
        present_baby = PresentBaby(baby_id=baby_id, date=datetime.now())
        db.add(present_baby)
        db.commit()
        return {
            "message": "Baby added to present successfully",
            "status_code": 200
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
def serialize_baby(baby: Baby) -> Dict[str, Any]:
    """ Serialize the Baby object to a dictionary. """
    return {
        "id": baby.id,
        "name": baby.name,
        "gender": baby.gender,
        "age": baby.age,
        "location": baby.location,
        "name_of_brought_person": baby.name_of_brought_person,
        "time_of_arrival": str(baby.time_of_arrival),
        "name_of_parent": baby.name_of_parent,
        "fee": baby.fee,
        "duration": baby.duration,
        "is_monthly": baby.is_monthly,
        "payment_type": baby.payment_type,
        "baby_access": baby.baby_access,
        "date": baby.date.isoformat(),
        "sitter_assigned": baby.sitter_assigned
    }

def get_present_babies(db: Session) -> Dict[str, Any]:
    print("Getting present babies")
    try:
        present_babies = db.query(PresentBaby).options(joinedload(PresentBaby.Baby)).all()
        if present_babies:
            serialized_babies = [serialize_baby(baby.Baby) for baby in present_babies]
            return {
                "message": "Babies retrieved successfully",
                "status_code": 200,
                "data": serialized_babies
            }
        else:
            return {
                "message": "No babies found",
                "status_code": 404,
                "data": []
            }
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))