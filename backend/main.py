from fastapi import FastAPI, HTTPException
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.product import router as products_router

import logging
from contextlib import asynccontextmanager
from os import path
from typing import AsyncGenerator
from starlette.middleware.cors import CORSMiddleware
from app.api.admin import router as admin_router


import uvicorn
from app.api.v1 import api_router
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


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    yield


app = FastAPI(
    title="Starter Kit Backend",
    lifespan=lifespan,
    summary="Starter Kit Backend Service",
    description="**Service Description**",
    version="0.0.1",
)

# -------------------------
# ROUTERS
# -------------------------
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])


# -------------------------
# MIDDLEWARE
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# EXCEPTION HANDLERS
# -------------------------
app.add_exception_handler(Exception, http_internal_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(ValidationError, request_custom_validation_exception_handler)

# -------------------------
# V1 API
# -------------------------
prefix_api_v1_version = "/api/v1"
app.include_router(api_router, prefix=prefix_api_v1_version)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=5051)
