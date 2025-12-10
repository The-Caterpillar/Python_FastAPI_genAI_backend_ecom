from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from dotenv import load_dotenv

from app.db.session import acquire_db_session as get_db
from app.core.security import get_current_user
from app.models.questionnaire import UserQuestionnaire
from app.models.persona import Persona
from app.utils.gemini_client import ask_gemini

from app.crud.persona import receive_persona, create_persona

import json

load_dotenv()
router = APIRouter()


@router.post("/generate")
async def generate_persona(
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user)
):
    try:
        result = await create_persona(db, user)
    except HTTPException:
        # Let the underlying HTTPException propagate (already meaningful)
        raise

    return result


@router.get("/Fetch Persona")
async def get_persona(
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user)
):
    received_persona = await receive_persona(db,user)

    if not received_persona:
        raise HTTPException(400, "Persona for this user does not exists as of yet.")
    return received_persona