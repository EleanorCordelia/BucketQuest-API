from fastapi import FastAPI
from app.routers.auth import router as auth_router

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="TST BucketQuest API",
    description="API for authentication and Supabase integration",
    version="1.0.0",
)

# Tambahkan router
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Endpoint root untuk testing
@app.get("/")
async def root():
    return {"message": "Welcome to TST BucketQuest API"}
