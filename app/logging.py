import logging

from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from pydantic import BaseModel, Field

from app.config import settings


class OTLPAuthConfig(BaseModel):
    """Class to hold OpenTelemetry authentication details."""

    endpoint: str
    bearer_token: str
    headers: dict = Field(default_factory=dict)
    
    def model_post_init(self, __context):
        """Set headers after initialization"""
        self.headers = {"authorization": f"Bearer {self.bearer_token}"}


def otel_trace_init(resource: Resource, otel_auth: OTLPAuthConfig) -> None:
    """Sets up OpenTelemetry trace exporter.

    Args:
        resource (Resource): The resource to be associated with all spans created.
        otel_endpoint (str): The endpoint to send traces to.
        otel_bearer_token (str): Bearer token to use for authentication.
    """
    tracer_provider = TracerProvider(resource=resource)

    otel_span_exporter = OTLPSpanExporter(
        endpoint=otel_auth.endpoint, headers=otel_auth.headers
    )
    span_processor = BatchSpanProcessor(otel_span_exporter)
    tracer_provider.add_span_processor(span_processor)

    trace.set_tracer_provider(tracer_provider)


def otel_logging_init(resource: Resource, otel_auth: OTLPAuthConfig) -> None:
    """Sets up OpenTelemetry log exporter.

    Args:
        resource (Resource): The resource to be associated with all spans created.
        otel_auth (dict): Dictionary containing the endpoint and bearer token for authentication.
    """
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)

    otel_log_exporter = OTLPLogExporter(
        endpoint=otel_auth.endpoint, headers=otel_auth.headers
    )
    log_processor = BatchLogRecordProcessor(otel_log_exporter)

    logger_provider.add_log_record_processor(log_processor)

    # Create OTEL log handler
    otel_log_handler = LoggingHandler(
        level=logging.INFO, logger_provider=logger_provider
    )

    root_logger = logging.getLogger()
    root_logger.addHandler(otel_log_handler)


def setup_loggers() -> None:
    """Setup loggers for the application."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    # Mimic the format of uvicorn logs
    console_formatter = logging.Formatter("%(levelname)s:     %(message)s - %(name)s")
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.INFO)
    app_logger.propagate = True  # Enable propagation to root logger

    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(logging.INFO)
    uvicorn_logger.propagate = True  # Enable propagation to root logger


def setup_opentelemetry():
    """
    Setup OpenTelemetry for log and trace exporting.
    """

    app_metadata = {
        "service.name": f"{settings['APP_NAME']}_{settings['ENV_NAME']}",
        "deployment.environment": settings["ENV_NAME"],
    }
    otlp_auth = OTLPAuthConfig(
        endpoint=settings["OTEL_ENDPOINT"],
        bearer_token=settings["OTEL_BEARER_TOKEN"],
    )

    resource = Resource.create(app_metadata)

    otel_trace_init(resource, otlp_auth)
    otel_logging_init(resource, otlp_auth)
