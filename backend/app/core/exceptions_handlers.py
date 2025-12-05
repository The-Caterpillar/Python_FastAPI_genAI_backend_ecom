import http
from fastapi.exceptions import RequestValidationError
from pydantic_core import ValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from app.core.base_response import BaseResponse


async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        BaseResponse.from_error_str(error=exc.detail).dict(),
        status_code=exc.status_code,
        headers=getattr(exc, "headers", None),
    )


async def http_internal_error_handler(_: Request, exc: Exception) -> JSONResponse:
    content = BaseResponse.from_error_str(
        error=http.HTTPStatus(HTTP_500_INTERNAL_SERVER_ERROR).phrase
    ).dict()
    return JSONResponse(content, status_code=HTTP_500_INTERNAL_SERVER_ERROR)


async def request_validation_exception_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    errors: list = []
    for item in exc.errors():
        errors.append(
            {
                "message": f"{item['loc']} - {item['msg']}",
                "detail": item["ctx"] if "ctx" in item else "",
            }
        )

    content = BaseResponse(errors=errors).dict()
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content=content,
    )


async def request_custom_validation_exception_handler(
    _: Request, exc: ValidationError
) -> JSONResponse:
    errors: list = []
    for item in exc.errors():
        errors.append(
            {
                "message": f"{item['loc']} - {item['msg']}",
                "detail": item["ctx"] if "ctx" in item else "",
            }
        )
    content = BaseResponse(errors=errors).dict()
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content=content,
    )
