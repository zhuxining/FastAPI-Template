from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.routing import APIRoute
from loguru import logger

from app.api.api import api_router
from app.core.config import settings
from app.core.db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    logger.add("logs/app_{time:YYYY-MM-DD}.log", rotation="1 day", retention="7 days", enqueue=True)
    logger.info("FastAPI app started")
    await create_db_and_tables()
    yield


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version=settings.VERSION,
    lifespan=lifespan,
    generate_unique_id_function=custom_generate_unique_id,
    debug=(settings.ENVIRONMENT == "dev"),
)

# CORS middleware
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if settings.ENVIRONMENT == "prod":
    app.add_middleware(HTTPSRedirectMiddleware)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.TRUSTED_HOSTS)

app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=6)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)
