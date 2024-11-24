from fastapi import FastAPI
from app.routers.auth import router as auth_router

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Tambahkan router
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Endpoint root
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI app"}
