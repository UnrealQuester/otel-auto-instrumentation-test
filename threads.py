import module
import threading
import mysql.connector
from opentelemetry.context import attach, get_current
from opentelemetry import trace
tracer = trace.get_tracer("my.tracer")

class _thread(threading.Thread):
    def run(self):
        if hasattr(self, '_otel_context'): attach(self._otel_context)
        with tracer.start_as_current_span("run"):
            c = mysql.connector.connect(
                host="127.0.0.1",
                port=3306,
                user="mike",
                password="s3cre3t!",
                database="test")
            cur = c.cursor()
            cur.execute("select * from test")
            res = cur.fetchall()

t = _thread()
t.start()
t.join()