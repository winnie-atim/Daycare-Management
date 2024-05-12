from fastapi import APIRouter, HTTPException, Depends
from Connections.connections import SessionLocal
from sqlalchemy.orm import Session
from Controllers.auth_controller import login_admin_controller
from Controllers.admin_controller import create_admin_controller
from Controllers.sitters_controller import create_sitter

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

@router.post("/login")
async def login_admin_route(admin_credentials: dict, db = Depends(get_db)):
    login = await login_admin_controller(db, admin_credentials)
    if login:
        return login
    else:
        raise HTTPException(status_code=400, detail="An error occurred")

@router.post("/admin_signup")
async def create_admin_route(admin: dict, db: Session = Depends(get_db)):
    try:
        created_admin = await create_admin_controller(db, admin)
        if created_admin:
            return created_admin
        else:
            raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
@router.post("/sitter_signup")
async def create_sitter_route(sitter: dict, db: Session = Depends(get_db)):
    try:
        created_sitted =  await create_sitter(db, sitter)
        if created_sitted:
            return {"message": "Sitter created successfully", "status": 200, "data": created_sitted}
        else:
            raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
