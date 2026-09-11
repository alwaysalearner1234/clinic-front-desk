"""Structured logging with correlation IDs."""
import logging
import sys
from typing import Any, Dict, Optional


class StructuredLogger:
    def __init__(self, name: str = "clinicfrontdesk"):
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def _sanitize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Strip sensitive credentials from logs."""
        clean = {}
        sensitive_keys = {"token", "auth", "secret", "password", "key", "sid"}
        for k, v in data.items():
            if any(s in k.lower() for s in sensitive_keys):
                clean[k] = "***REDACTED***"
            else:
                clean[k] = v
        return clean

    def info(self, message: str, correlation_id: Optional[str] = None, **kwargs: Any) -> None:
        sanitized = self._sanitize(kwargs)
        extra_str = f" | {sanitized}" if sanitized else ""
        cid_str = f"[{correlation_id}] " if correlation_id else ""
        self.logger.info(f"{cid_str}{message}{extra_str}")

    def warning(self, message: str, correlation_id: Optional[str] = None, **kwargs: Any) -> None:
        sanitized = self._sanitize(kwargs)
        extra_str = f" | {sanitized}" if sanitized else ""
        cid_str = f"[{correlation_id}] " if correlation_id else ""
        self.logger.warning(f"{cid_str}{message}{extra_str}")

    def error(self, message: str, correlation_id: Optional[str] = None, **kwargs: Any) -> None:
        sanitized = self._sanitize(kwargs)
        extra_str = f" | {sanitized}" if sanitized else ""
        cid_str = f"[{correlation_id}] " if correlation_id else ""
        self.logger.error(f"{cid_str}{message}{extra_str}")

    def debug(self, message: str, correlation_id: Optional[str] = None, **kwargs: Any) -> None:
        sanitized = self._sanitize(kwargs)
        extra_str = f" | {sanitized}" if sanitized else ""
        cid_str = f"[{correlation_id}] " if correlation_id else ""
        self.logger.debug(f"{cid_str}{message}{extra_str}")


logger = StructuredLogger()
