from fastapi import HTTPException
from Controllers.admin_controller import (
    login_admin
)

async def login_admin_controller(db, admin_credentials):
    try:
        logged_admin = await login_admin(db, admin_credentials)
        if logged_admin:
            return logged_admin
        else:
            raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")