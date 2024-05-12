from Models.models import Payment
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

async def create_payment(db_session: Session, payment: dict):
    try:
        new_payment = Payment.create_payment(db_session, payment)
        return {
            "message": "Payment created successfully",
            "status_code": 200,
            "data": { "payment_id": new_payment.id,
                     "amount": new_payment.amount,
                     "payment_date": new_payment.payment_date,
                     "baby_id": new_payment.baby_id,
                     "sitter_id": new_payment.sitter_id
                    }
        }
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")