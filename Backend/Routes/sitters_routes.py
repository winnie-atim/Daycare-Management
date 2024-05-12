from fastapi import APIRouter, HTTPException, Depends
from Connections.connections import SessionLocal
from sqlalchemy.orm import Session

from Controllers.sitters_controller import (
    create_sitter
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
