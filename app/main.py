import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.logging import setup_loggers, setup_opentelemetry
from app.routers.v1 import v1_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def setup(app: FastAPI):
    """
    Setup function to initialize the FastAPI application.
    """
    setup_loggers()
    setup_opentelemetry()
    logger.info("OpenTelemetry initialized")
    yield


app = FastAPI(lifespan=setup)
app.include_router(v1_router)

FastAPIInstrumentor.instrument_app(
    app,
    excluded_urls="/health,/metrics",
)
