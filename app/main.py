from fastapi import FastAPI
from app.routers.v1 import v1_router
from app.logging import setup_opentelemetry
import logging

logger = logging.getLogger(__name__)


def setup():
    """
    Setup function to initialize the FastAPI application.
    """
    # Initialize OpenTelemetry
    setup_opentelemetry()
    logger.info("OpenTelemetry initialized")
    yield


app = FastAPI(lifespan=setup)
app.include_router(v1_router)
