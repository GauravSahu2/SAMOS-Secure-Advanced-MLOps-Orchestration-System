"""
src/logging_config.py — Unified SAMOS Logging Configuration (Gap #25)

Usage in any module:
    from src.logging_config import get_logger
    logger = get_logger(__name__)

This replaces the scattered mix of print() / logging.basicConfig() calls
with a single, project-wide configuration that respects the LOG_LEVEL
environment variable.
"""

import logging
import os
import sys

import json

_LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
_LOG_FORMAT = os.environ.get("LOG_FORMAT", "text").lower()

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def _setup_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    if _LOG_FORMAT == "json":
        handler.setFormatter(JSONFormatter(datefmt="%Y-%m-%dT%H:%M:%SZ"))
    else:
        handler.setFormatter(logging.Formatter(
            fmt="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s", 
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
    
    logging.basicConfig(
        level=getattr(logging, _LOG_LEVEL, logging.INFO),
        handlers=[handler],
        force=True,     # Override any earlier basicConfig calls
    )

_setup_logging()

# Silence overly noisy third-party loggers
for _noisy in ("transformers", "datasets", "huggingface_hub", "urllib3", "fsspec"):
    logging.getLogger(_noisy).setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Returns a named logger configured at the project-wide LOG_LEVEL.

    Args:
        name: Typically `__name__` of the calling module.

    Returns:
        A standard Python Logger instance.
    """
    return logging.getLogger(name)
