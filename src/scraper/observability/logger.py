# scraper/observability/logging.py
import json
import logging
import sys
import uuid
from contextvars import ContextVar
from datetime import datetime, timezone

# Holds the current run's ID. ContextVar (not a global or thread-local)
# because it propagates correctly across async tasks — which matters
# the moment you move to aiohttp.
_run_id: ContextVar[str] = ContextVar("run_id", default="-")

# Standard LogRecord attributes — anything NOT in here was passed by you
# via extra={...} and should appear in the JSON output.
_STANDARD = set(logging.makeLogRecord({}).__dict__) | {
    "message", "asctime", "taskName"}


def new_run_id() -> str:
    rid = uuid.uuid4().hex[:12]
    _run_id.set(rid)
    return rid

# inject the run_id into every log record, so we don't have to pass it around manually


class RunIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.run_id = _run_id.get()
        return True


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "run_id": getattr(record, "run_id", "-"),
            "event": record.getMessage(),
        }
        for key, value in record.__dict__.items():
            if key not in _STANDARD and key not in payload:
                payload[key] = value
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False, default=str)


def configure_logging(level: int = logging.INFO, *, json_output: bool = True) -> None:
    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()  # avoid duplicate handlers on re-configure
    handler = logging.StreamHandler(sys.stdout)
    handler.addFilter(RunIdFilter())
    if json_output:
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s [%(run_id)s] %(name)s: %(message)s")
        )
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
