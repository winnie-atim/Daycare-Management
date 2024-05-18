from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.middleware.cors import CORSMiddleware
from Routes import (
    sitters_routes,
    baby_routes,
    admin_routes,
    auth_routes
)
from apscheduler.triggers.cron import CronTrigger
import uvicorn
from datetime import datetime
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Baby": "App"}

app.include_router(sitters_routes.router, prefix="/sitters")#, tags=["Sitters"])
app.include_router(baby_routes.router, prefix="/babies")#, tags=["Babies"])
app.include_router(admin_routes.router, prefix="/admins")#, tags=["Admins"])
app.include_router(auth_routes.router, prefix="/auth")#, tags=["Auth"])

# Initializing the scheduler
scheduler = BackgroundScheduler()

# Defining the task
def reset_sitter_status():
    import requests
    try:
        response = requests.get('http://127.0.0.1:8014/sitters/get_all_sitters')
        sitters = response.json()['data']

        for sitter in sitters:
            sitter_id = sitter['id']
            requests.put(f'http://127.0.0.1:8014/sitters/new_day_sitter/?sitter_id={sitter_id}')
        print(f"Sitters' status reset successfully at {datetime.now()}.")
    except requests.RequestException as e:
        print(f"Failed to reset sitters' status: {e}")

# Schedule the task
scheduler.add_job(reset_sitter_status, CronTrigger(hour=0, minute=0))  
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8014, reload=True)
