from fastapi import APIRouter, HTTPException, Depends
from Connections.connections import SessionLocal
from sqlalchemy.orm import Session
from Controllers.baby_controller import (
    create_baby_controller,
    update_baby,
    relaese_baby
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
    return {"Babies" : "Hello World"}

@router.post("/create_baby")
async def create_baby_route(baby: dict, db: Session = Depends(get_db)):
    try:
        created_baby = create_baby_controller(db, baby)
        if created_baby:
            return created_baby
        else:
            raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: Heres {e}")
    
@router.put("/update_baby")
async def update_existing_baby(baby_data: dict, db: Session = Depends(get_db)):
    try:
        updated_baby = update_baby(db, baby_data)
        if updated_baby:
            return updated_baby
        else:
            raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
@router.post("/release_baby")
async def realase_baby_route(baby_data: dict, db: Session = Depends(get_db)):
    try:
        release = relaese_baby(db, baby_data)
        if release:
            return release
        else:
            raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    