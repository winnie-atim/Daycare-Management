from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.middleware.cors import CORSMiddleware
from Routes import (
    sitters_routes,
    baby_routes,
    admin_routes,
    auth_routes
)
import tasks
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

# # Initializing the scheduler
# scheduler = BackgroundScheduler()



# scheduler.add_job(tasks.reset_sitter_status, CronTrigger(hour=0, minute=0))
# scheduler.add_job(tasks.reset_daily_payments, CronTrigger(hour=0, minute=0))  
# scheduler.start()

# @app.on_event("shutdown")
# def shutdown_event():
#     scheduler.shutdown()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8014, reload=True)
