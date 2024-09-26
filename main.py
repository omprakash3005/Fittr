from fastapi import FastAPI
from app.user.routes import router as users_router
from app.Admin.routes import router as admin_router
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])