from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import acquire_db_session as get_db
from app.core.security import get_current_user
from app.models.questionnaire import UserQuestionnaire

router = APIRouter()

# Hardcoded 5 questions (used for validation only)
QUESTIONNAIRE = [
    "How would you describe your personal style?",
    "What motivates you when buying a product?",
    "What colors or aesthetics do you naturally gravitate toward?",
    "What frustrates you most when shopping?",
    "What do you usually hope a product will make you feel?"
]


# New format: answers is a dict {question: user_answer}
class QuestionnaireAnswers(BaseModel):
    answers: dict[str, str]

    class Config:
        json_schema_extra = {
            "example": {
                "answers": {
                    "How would you describe your personal style?": "casual and elegant",
                    "What motivates you when buying a product?": "Necessity",
                    "What colors or aesthetics do you naturally gravitate toward?": "mustard yellow, white, hot pink, bright red",
                    "What frustrates you most when shopping?": "Sizing issues! WHY IS EVERYTHING CROPPED?",
                    "What do you usually hope a product will make you feel?": "comfortable and elegant"
                }
            }
        }


@router.post("/submit")
async def submit_questionnaire(
    payload: QuestionnaireAnswers,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    answers_dict = payload.answers

    # Validate question count
    if len(answers_dict) != 5:
        raise HTTPException(400, detail="All 5 questions must be answered.")

    # Validate keys match questionnaire
    if set(answers_dict.keys()) != set(QUESTIONNAIRE):
        raise HTTPException(
            400,
            detail="Submitted questions do not match the expected questionnaire."
        )

    # Fetch existing entry
    stmt = select(UserQuestionnaire).where(UserQuestionnaire.user_id == user.id)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        existing.answers = answers_dict
    else:
        new_entry = UserQuestionnaire(
            user_id=user.id,
            answers=answers_dict
        )
        db.add(new_entry)

    await db.commit()

    return {"status": "saved", "answers": answers_dict}
