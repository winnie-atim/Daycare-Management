from fastapi import APIRouter, HTTPException, Depends
from Connections.connections import get_db
from sqlalchemy.orm import Session

from Controllers.admin_controller import (
    create_admin_controller,
    generate_signup_token,
    generate_reset_token,
    reset_password
)

router = APIRouter()

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
        return created_admin
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    

@router.post("/generate_reset_token")
async def generate_reset_token_route(email: str, db: Session = Depends(get_db)):
    try:
        result = await generate_reset_token(db, email)
        if result:
            return {"message": "Reset link sent successfully", "status_code": 200}
        else:
            raise HTTPException(status_code=400, detail="Failed to send reset link")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
@router.post("/reset_password")
async def reset_password_route(user_data: dict, db: Session = Depends(get_db)):
    token = user_data.get("token")
    password = user_data.get("password")
    try:
        valid_token = reset_password(db, token, password)
        if valid_token:
            return valid_token
        else:
            raise HTTPException(status_code=400, detail="Invalid token")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
