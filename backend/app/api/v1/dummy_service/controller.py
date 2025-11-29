from fastapi import HTTPException, status
from backend.config.config import config
from json import loads, dumps
import logging
from backend.db.base import session
from datetime import datetime
import pytz
from sqlalchemy.exc import IntegrityError
from pprint import pprint
from backend.common.time_utility import current_time_in_GMT
from backend.utils.file_reader import load_json_file
from typing import List, Optional, Dict, Any
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class ExceptionCustom(HTTPException):
    pass


class DummyService:

    def __init__(self):
        pass

    async def create_dummy(self, session: AsyncSession):
        try:
            pass
        except Exception as e:
            logger.error(f"Error creating chat session: {str(e)}")
            raise ExceptionCustom(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create chat session",
            )
