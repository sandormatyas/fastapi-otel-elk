from fastapi import FastAPI
from app.routers.v1 import v1_router
from app.logging import setup_opentelemetry
import logging
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def setup(app: FastAPI):
    """
    Setup function to initialize the FastAPI application.
    """
    # Initialize OpenTelemetry
    setup_opentelemetry()
    logger.info("OpenTelemetry initialized")
    yield


app = FastAPI(lifespan=setup)
app.include_router(v1_router)

FastAPIInstrumentor.instrument_app(
    app,
    excluded_urls="/health,/metrics",
)
