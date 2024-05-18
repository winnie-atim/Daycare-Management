from fastapi import APIRouter, HTTPException, Depends
from Connections.connections import SessionLocal
from sqlalchemy.orm import Session
from Controllers.baby_controller import (
    create_baby_controller,
    update_baby,
    relaese_baby,
    get_all_babies,
    add_baby_to_present,
    get_present_babies,
    get_released_babies,
    get_baby_by_access
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
            add_baby_to_present(db, created_baby['data'].id)
            return {
                "message": "Baby registered successfully",
                "status_code": 200,
                "data": {
                    "id": created_baby['data'].id,
                    "name": created_baby['data'].name,
                    "gender": created_baby['data'].gender,
                    "age": created_baby['data'].age,
                    "location": created_baby['data'].location,
                    "name_of_brought_person": created_baby['data'].name_of_brought_person,
                    "time_of_arrival": created_baby['data'].time_of_arrival,
                    "name_of_parent": created_baby['data'].name_of_parent,
                    "fee": created_baby['data'].fee,
                    "sitter_assigned": created_baby['data'].sitter_assigned,
                    "baby_access": created_baby['data'].baby_access
                }
            }
        else:
            raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: Heres {e}")
    
@router.put("/update_baby")
async def update_existing_baby(baby_data: dict, db: Session = Depends(get_db)):
    try:
        updated_baby = update_baby(db, baby_data)
        if updated_baby:
            add_baby_to_present(db, updated_baby.id)
            return {"status_code": 200, "message": "Baby updated successfully", "data": updated_baby}
        else:
            raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.get("/get_all_babies")
async def get_all_babies_route(db: Session = Depends(get_db)):
    try:
        babies = get_all_babies(db)
        if babies:
            return babies
        else:
            raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
@router.get("/get_all_present_babies")
async def get_present_babies_route(db: Session = Depends(get_db)):
    try:
        present_babies = get_present_babies(db)
        if present_babies:
            return present_babies
        else:
            raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.get("/get_baby_by_access")
async def get_baby_by_access_route(baby_access: str, db: Session = Depends(get_db)):
    try:
        baby = get_baby_by_access(db, baby_access)
        if baby:
            return baby
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
    
@router.get('/get_release_baby')
async def get_released_babies_route(db: Session = Depends(get_db)):
    try:
        relaese_baby = get_released_babies(db)
        if relaese_baby:
            return relaese_baby
        else:
            raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    