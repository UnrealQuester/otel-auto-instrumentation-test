import os
import sys
import atexit
import inspect
import threading

parent = next(inspect.getmodule(f[0]).__file__ for f in inspect.stack()[1:] if not f.filename.startswith('<'))

os.environ["OTEL_TRACES_EXPORTER"] = "console"
os.environ["OTEL_SERVICE_NAME"] = parent
os.environ["OTEL_SDK_DISABLED"] = "false"
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

def handle_exception(exc_type, exc_value, exc_traceback):
    span.record_exception(exc_value)
    span.set_status(trace.Status(trace.StatusCode.ERROR, str(exc_value)))
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

def handle_threading_exception(args: threading.ExceptHookArgs):
    trace.get_current_span().record_exception(args.exc_value)
    trace.get_current_span().set_status(trace.Status(trace.StatusCode.ERROR, str(args.exc_value)))
    threading.__excepthook__(args)

sys.excepthook = handle_exception
threading.excepthook = handle_threading_exception

# from opentelemetry.instrumentation.mysql import MySQLInstrumentor

# # Call instrument() to wrap all database connections
# MySQLInstrumentor().instrument(tracer_provider=trace.get_tracer_provider())