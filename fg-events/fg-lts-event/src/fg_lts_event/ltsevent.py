"""LTS event class for FunctionGraph."""

import base64
import json


class LTSEvent:
    """Represents an LTS event for FunctionGraph."""

    def __init__(self, event):
        self._event = event or {}

    def get_raw_data(self):
        return (self._event.get("lts") or {}).get("data") or ""

    def get_data(self):
        try:
            # LTS delivers the payload as base64-encoded UTF-8 text.
            decoded = base64.b64decode(self.get_raw_data())
            return decoded.decode("utf-8")
        except Exception:
            return ""

    def get_logs(self):
        try:
            json_data = json.loads(self.get_data())
            # Invalid or partial payloads are treated as having no log entries.
            return json_data.get("logs") or []
        except (json.JSONDecodeError, TypeError, AttributeError):
            return []

    def to_json(self):
        return self._event


__all__ = ["LTSEvent"]