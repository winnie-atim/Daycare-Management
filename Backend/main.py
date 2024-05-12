from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Routes import (
    sitters_routes,
    baby_routes,
    admin_routes,
    auth_routes
)

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
if __name__ == "__main__":
    import uvicorn
    from watchgod import watch 
    uvicorn.run("main:app", host="127.0.0.1", port=8014, reload=True)