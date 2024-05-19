from fastapi import APIRouter, HTTPException, Depends
from Connections.connections import SessionLocal
from sqlalchemy.orm import Session

from Controllers.admin_controller import (
    create_admin_controller,
    generate_signup_token
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def read_root():
    return {"Admins" : "Hello World"}

@router.post("/generate_signup_token")
async def generate_signup_token_for_admin(emailbody: dict):
    email = emailbody["email"]
    admin_id = emailbody["admin_id"]
    try:
        return_data = await generate_signup_token(email,admin_id,"admin")
        if return_data:
            return {
                "message": "Token generated successfully",
                "status_code": 200,
                "data" : {
                "id": return_data["id"],
                "email": email, 
                "token": return_data["token"],
                "status": return_data["status"],
                "time": return_data["time"],
                "added_by": return_data["added_by"],
                }
            }
           
        else:
            raise HTTPException(status_code=400, detail="Unable to generate token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create_admin")
async def create_admin_route(admin: dict, db: Session = Depends(get_db)):
    try:
        created_admin = await create_admin_controller(db, admin)
        if created_admin:
            return created_admin
        else:
            raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
