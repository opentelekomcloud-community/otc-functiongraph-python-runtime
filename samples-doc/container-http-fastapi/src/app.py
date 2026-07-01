from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse

from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.middleware.cors import CORSMiddleware

import logging
import logging.config
from api.items import items_router
from asgi_correlation_id import CorrelationIdMiddleware, correlation_id
import time

from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse

import traceback
import os

ROOT_LEVEL = os.environ.get("RUNTIME_LOG_LEVEL", "DEBUG").upper()


class UTCFormatter(logging.Formatter):
    converter = time.gmtime

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
        "correlation_id": {
            "()": "asgi_correlation_id.CorrelationIdFilter",
            "uuid_length": 36,
            "default_value": "-",
        },
    },
    "formatters": {
        "standard": {
            "()": UTCFormatter,
            "format": "%(asctime)s.%(msecs)03dZ [%(levelname)s] [%(correlation_id)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "level": ROOT_LEVEL,
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "filters": ["correlation_id"],
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {
        "": {  # root logger
            "level": ROOT_LEVEL,  # "INFO",
            "handlers": ["default"],
            "propagate": False,
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["default"],
        },
        "uvicorn.access": {
            "level": ROOT_LEVEL,
            "handlers": ["default"],
            "propagate": False,
        },
    },
}

logger = logging.getLogger(__name__)

tags_metadata = [
    {"name": "API", "description": "API samples"},
]


# see: https://fastapi.tiangolo.com/advanced/events/?h=async+conte#lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    logging.config.dictConfig(LOGGING_CONFIG)
    yield
    # cleanup


app = FastAPI(
    lifespan=lifespan,
    title="FunctionGraph and FastAPI",
    summary="T Cloud Public sample for FunctionGraph HTTP function using FastAPI",
    version="0.0.1",
    debug=True,
    docs_url=None,  # will be overwritten, see below: overridden_swagger()
    redoc_url=None,  # will be overwritten, see below: overridden_redoc()
    openapi_tags=tags_metadata,
)


@app.get("/docs", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url, title=app.title, swagger_favicon_url="/favicon.ico"
    )


@app.get("/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(
        openapi_url=app.openapi_url, title=app.title, redoc_favicon_url="/favicon.ico"
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(traceback.format_exc())

    return await http_exception_handler(
        request,
        HTTPException(
            500,
            "Internal server error",
            headers={"x-cff-request-id": correlation_id.get() or ""},
        ),
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# add requestid to logging, see: https://github.com/snok/asgi-correlation-id
app.add_middleware(CorrelationIdMiddleware, header_name="x-cff-request-id")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=[
        # "X-Requested-With",
        # "X-Request-ID",
        # "x-cff-request-id",
        # "x-cff-security-access-key",
        # "x-cff-security-secret-key",
        # "x-cff-security-token",
        "Access-Control-Allow-Origin",
        "Access-Control-Expose-Headers",
    ],
    expose_headers=[
        # "X-Request-ID",
        # "x-cff-request-id",
        "Access-Control-Allow-Origin",
        "Access-Control-Expose-Headers",
    ],
)

@app.get("/")
def read_root(request: Request):
    headers = request.headers
    logging.debug("Debug hello")

    logging.debug("Request headers: %s", dict(headers))
    
    ak = headers.get("x-cff-security-access-key")
    sk = headers.get("x-cff-security-secret-key")
    st = headers.get("x-cff-security-token")
    token = headers.get("x-cff-auth-token")
    
    if ak and ak != "null":
        logging.info("Access Key is: %s", ak)
    else:
        logging.error("NO AGENCY SPECIFIED OR KEYS NOT INCLUDED")
        
    return {"Hello": "World", "Agency ok": ak is not None and ak != "null", "Request ID": correlation_id.get() or ""}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(
        "./static/favicon.ico", media_type="image/x-icon", filename="favicon.ico"
    )


app.include_router(items_router, prefix="/api", tags=["API"])

if __name__ == "__main__":
    import uvicorn

    #uvicorn.run("app:app", port=8000, log_level="debug", reload=True, host="localhost")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug", log_config=LOGGING_CONFIG, reload=False)
