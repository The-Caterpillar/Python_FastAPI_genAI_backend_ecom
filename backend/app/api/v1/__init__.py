from fastapi import APIRouter
from app.api.v1.status.route import StatusRouter

api_router = APIRouter()

api_router.include_router(StatusRouter.status_router)
