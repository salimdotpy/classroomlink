
import logging

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.core.templates import templates

logger = logging.getLogger(__name__)

def wants_json(request: Request) -> bool:
    """
    Determine whether the client expects a JSON response.
    """

    if request.url.path.startswith("/api/"):
        return True

    accept = request.headers.get("accept", "")

    return (
        "application/json" in accept
        and "text/html" not in accept
    )

async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
):
    """
    Handle HTTP exceptions.
    """

    if wants_json(request):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers,
        )

    messages = {
        400: "The request could not be processed.",
        401: "Please authenticate to access this resource.",
        403: "You do not have permission to access this resource.",
        404: "The page you are looking for could not be found.",
        405: "This action is not supported.",
        429: "Too many requests. Please try again later.",
        500: "Something went wrong while processing your request.",
        503: "The service is temporarily unavailable.",
    }

    return templates.TemplateResponse(
        request=request,
        name="errors/error.html",
        context={
            "app_name": settings.app_name,
            "status_code": exc.status_code,
            "title": "Request Error",
            "message": messages.get(
                exc.status_code,
                "Your request could not be completed.",
            ),
        },
        status_code=exc.status_code,
        headers=exc.headers,
    )

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    """
    Handle request validation errors.
    """

    if wants_json(request):
        return JSONResponse(
            status_code=422,
            content={
                "detail": jsonable_encoder(exc.errors()),
            },
        )

    return templates.TemplateResponse(
        request=request,
        name="errors/error.html",
        context={
            "app_name": settings.app_name,
            "status_code": 422,
            "title": "Invalid Request",
            "message": (
                "Some of the information provided was invalid. "
                "Please check your request and try again."
            ),
        },
        status_code=422,
    )

async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Handle unexpected application errors.
    """

    logger.exception(
        "Unhandled exception at %s",
        request.url.path,
        exc_info=exc,
    )

    if wants_json(request):
        return JSONResponse(
            status_code=500,
            content={
                "detail": "An unexpected error occurred."
            },
        )

    return templates.TemplateResponse(
        request=request,
        name="errors/error.html",
        context={
            "app_name": settings.app_name,
            "status_code": 500,
            "title": "Something Went Wrong",
            "message": (
                "We encountered an unexpected problem. "
                "Please try again later."
            ),
        },
        status_code=500,
    )

def register_exception_handlers(app: FastAPI) -> None:
    """
    Register application-wide exception handlers.
    """

    app.add_exception_handler(
        StarletteHTTPException,
        http_exception_handler,
    )

    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        unexpected_exception_handler,
    )