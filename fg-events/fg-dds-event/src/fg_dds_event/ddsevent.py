"""DDS event classes for FunctionGraph."""

import json


class DDSEvent:
    """Represents a DDS event for FunctionGraph."""

    def __init__(self, event):
        self._event = event or {}
        self._records = [DDSRecord(record) for record in self._event.get("records") or []]

    def get_records(self):
        return self._records

    def get_record(self, index):
        if 0 <= index < len(self._records):
            return self._records[index]
        return None

    def to_json(self):
        return self._event


class DDSRecord:
    """Represents a single DDS event record."""

    def __init__(self, record):
        self._record = record or {}

    def get_event_source(self):
        return self._record.get("event_source") or ""

    def get_event_version(self):
        return self._record.get("event_version") or ""

    def get_event_name(self):
        return self._record.get("event_name") or ""

    def get_event_source_ip(self):
        return self._record.get("event_source_ip") or ""

    def get_region(self):
        return self._record.get("region") or ""

    def get_dds(self):
        return DDS(self._record.get("dds"))

    def to_json(self):
        return self._record


class DDS:
    """Represents the DDS payload of an event record."""

    def __init__(self, dds):
        self._dds = dds or {}

    def get_size_bytes(self):
        return self._dds.get("size_bytes") or 0

    def get_token_raw(self):
        return self._dds.get("token") or ""

    def get_token(self):
        return _parse_json_value(self._dds.get("token"), {})

    def get_full_document_raw(self):
        return self._dds.get("full_document") or {}

    def get_full_document(self):
        return _parse_json_value(self._dds.get("full_document"), {})

    def get_ns_raw(self):
        return self._dds.get("ns") or ""

    def get_ns(self):
        return _parse_json_value(self._dds.get("ns"), {})

    def to_json(self):
        return self._dds


def _parse_json_value(value, default):
    if isinstance(value, (dict, list)):
        return value

    try:
        return json.loads(value or "{}")
    except (json.JSONDecodeError, TypeError):
        return default


__all__ = ["DDSEvent", "DDSRecord", "DDS"]