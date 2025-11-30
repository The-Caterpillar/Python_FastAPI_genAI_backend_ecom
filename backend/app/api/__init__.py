from app.api.auth import router as auth_router
from fastapi import FastAPI, HTTPException, APIRouter

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])