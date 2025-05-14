import logging
from app.config import settings

from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def otel_trace_init(resource: Resource, otel_endpoint: str, otel_bearer_token: str):
    """Sets up OpenTelemetry trace exporter.

    Args:
        resource (Resource): The resource to be associated with all spans created.
        otel_endpoint (str): The endpoint to send traces to.
        otel_bearer_token (str): Bearer token to use for authentication.
    """
    tracer_provider = TracerProvider(resource=resource)

    otel_span_exporter = OTLPSpanExporter(
        endpoint=otel_endpoint,
        headers={"authorization": f"Bearer {otel_bearer_token}"},
    )
    span_processor = BatchSpanProcessor(otel_span_exporter)
    tracer_provider.add_span_processor(span_processor)

    trace.set_tracer_provider(tracer_provider)


def otel_logging_init(resource: Resource, otel_endpoint: str, otel_bearer_token: str):
    """Sets up OpenTelemetry log exporter.

    Args:
        resource (Resource): The resource to be associated with all spans created.
        otel_endpoint (str): The endpoint to send traces to.
        otel_bearer_token (str): Bearer token to use for authentication.
    """
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)

    otel_log_exporter = OTLPLogExporter(
        endpoint=otel_endpoint,
        headers={"authorization": f"Bearer {otel_bearer_token}"},
    )
    log_processor = BatchLogRecordProcessor(otel_log_exporter)

    logger_provider.add_log_record_processor(log_processor)

    otel_log_handler = LoggingHandler(
        level=logging.INFO, logger_provider=logger_provider
    )
    logging.getLogger().addHandler(otel_log_handler)
    logging.getLogger("app").addHandler(otel_log_handler)
    logging.getLogger("uvicorn").addHandler(otel_log_handler)


def setup_opentelemetry():
    """
    Setup OpenTelemetry for logging.
    """

    app_metadata = {
        "service.name": f"{settings['APP_NAME']}_{settings['ENV_NAME']}",
        "deployment.environment": settings["ENV_NAME"],
    }

    resource = Resource.create(app_metadata)

    otel_trace_init(resource, settings["OTEL_ENDPOINT"], settings["OTEL_BEARER_TOKEN"])
    otel_logging_init(
        resource, settings["OTEL_ENDPOINT"], settings["OTEL_BEARER_TOKEN"]
    )
