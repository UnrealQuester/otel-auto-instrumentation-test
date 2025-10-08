import os
import atexit
import inspect

parent = next(inspect.getmodule(f[0]).__file__ for f in inspect.stack()[1:] if not f.filename.startswith('<'))

os.environ["OTEL_TRACES_EXPORTER"] = "console"
os.environ["OTEL_SERVICE_NAME"] = parent
from opentelemetry.instrumentation import auto_instrumentation
auto_instrumentation.initialize()
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.resources import Resource
# from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor

from opentelemetry import trace, context

# trace.set_tracer_provider(
#     TracerProvider(resource=Resource.create({"service.name": parent}))
# )
# trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
span = trace.get_tracer("asdf").start_span(name="parent")
ctx = trace.set_span_in_context(span)
context.attach(ctx)

@atexit.register
def endSpan():
    span.end()

# from opentelemetry.instrumentation.mysql import MySQLInstrumentor

# # Call instrument() to wrap all database connections
# MySQLInstrumentor().instrument(tracer_provider=trace.get_tracer_provider())