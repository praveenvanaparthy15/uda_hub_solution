import json
import logging
from pathlib import Path
from datetime import datetime


LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "uda_hub.log"


class JsonFormatter(logging.Formatter):
    """Format log records as JSON."""

    def format(self, record):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        if hasattr(record, "agent"):
            log_entry["agent"] = record.agent

        if hasattr(record, "ticket_id"):
            log_entry["ticket_id"] = record.ticket_id

        return json.dumps(log_entry)


logger = logging.getLogger("uda_hub")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)


def log_event(
    message: str,
    agent: str = "system",
    ticket_id=None,
):
    """Write a structured event to the UDA-Hub log."""

    logger.info(
        message,
        extra={
            "agent": agent,
            "ticket_id": ticket_id,
        },
    )