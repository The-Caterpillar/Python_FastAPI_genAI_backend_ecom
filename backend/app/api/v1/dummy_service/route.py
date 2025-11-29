import logging
from fastapi import (
    File,
    Path,
    Query,
    APIRouter,
    HTTPException,
    UploadFile,
    status,
    Depends,
)
from backend.api.v1.dummy_service.controller import ChatbotService
from typing import Annotated
from backend.config.config import config
from backend.core.base_response import BaseResponse
from backend.db.session import acquire_db_session
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class ExceptionCustom(HTTPException):
    pass


dummy_router = APIRouter(
    prefix="/dummy",
    tags=["Dummy Service"],
)
dummy_service = ChatbotService()


@dummy_router.post(
    "/dummy",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create a new chat session",
)
async def create_dummy(
    session: AsyncSession = Depends(acquire_db_session),
):
    try:
        pass
    except ExceptionCustom as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        )
    except Exception as e:
        logger.error(f"Error in create_dummy: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
