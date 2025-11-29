import logging
from typing import Dict

from fastapi import APIRouter

from backend.app.schemas.status import ServiceStatusSchema

logger = logging.getLogger(__name__)


class StatusRouter:
    status_router = APIRouter(
        prefix="/status",
        tags=["Status"],
    )

    @staticmethod
    @status_router.get(
        "/",
        response_model=ServiceStatusSchema,
        summary="Check Status of the Service",
        description="**Description**",
    )
    def get() -> Dict[str, str]:
        logger.info("Status call executed")
        return {"message": "OK"}
