from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import FastAPI, HTTPException
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.product import router as products_router
from app.api.questionnaire import router as questionnaire_router
from app.api.persona import router as persona_router
from dotenv import load_dotenv
load_dotenv()
from fastapi.responses import HTMLResponse
import logging
from contextlib import asynccontextmanager
from os import path
from typing import AsyncGenerator
from starlette.middleware.cors import CORSMiddleware
from app.api.admin import router as admin_router
import uvicorn
from app.core.exceptions_handlers import (
    http_exception_handler,
    http_internal_error_handler,
    request_custom_validation_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from pydantic_core import ValidationError

log_file_path = path.join(
    path.dirname(path.abspath(__file__)), "app/core/logging.conf"
)
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

# @asynccontextmanager
# async def lifespan(_: FastAPI) -> AsyncGenerator:
#     yield


app = FastAPI(
    title="Python Backend",
    summary="",
    description="*",
    version="1.0.0",
    docs_url=None,   # to disable default Swagger
    redoc_url=None   # to disable ReDoc
)

# Mount Static Files - for UI part
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
# Custom Swagger UI
from pathlib import Path
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    file_path = Path(__file__).parent / "static" / "swagger.html"
    html = file_path.read_text()
    return HTMLResponse(html)


# Each line registers an API module (router) with my FastAPI app.
# ROUTERS
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(questionnaire_router, prefix="/questionnaire", tags=["Questionnaire"])
app.include_router(persona_router, prefix="/persona", tags=["Persona"])



# It enables CORS (Cross-Origin Resource Sharing).
# MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# This lets your frontend communicate with your backend without browser blocking it.




# EXCEPTION HANDLERS - core
app.add_exception_handler(Exception, http_internal_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(ValidationError, request_custom_validation_exception_handler)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=5051)
