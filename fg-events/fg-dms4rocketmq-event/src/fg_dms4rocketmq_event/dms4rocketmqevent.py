"""DMS RocketMQ event classes for FunctionGraph."""


class DMS4RocketMQEvent:
    """Represents a DMS4RocketMQ event for FunctionGraph."""

    def __init__(self, event):
        self._event = event or {}

    def get_event_version(self):
        return self._event.get("event_version") or ""

    def get_event_time(self):
        return self._event.get("event_time") or ""

    def get_region(self):
        return self._event.get("region") or ""

    def get_trigger_type(self):
        return self._event.get("trigger_type") or ""

    def get_instance_id(self):
        return self._event.get("instance_id") or ""

    def get_records(self):
        return [DMS4RocketMQRecord(record) for record in self._event.get("records") or []]

    def to_json(self):
        return self._event


class DMS4RocketMQRecord:
    """Represents a topic record in a DMS4RocketMQ event."""

    def __init__(self, record):
        self._record = record or {}
        self._messages = [
            DMS4RocketMQRecordMessage(message) for message in self._record.get("messages") or []
        ]

    def get_topic_id(self):
        return self._record.get("topic_id") or ""

    def get_messages(self):
        return self._messages

    def to_json(self):
        return self._record


class DMS4RocketMQRecordMessage:
    """Represents a single message in a DMS4RocketMQ record."""

    def __init__(self, record):
        self._record = record or {}

    def get_message(self):
        if isinstance(self._record, str):
            return self._record
        return self._record.get("message") or ""

    def to_json(self):
        return self._record


__all__ = [
    "DMS4RocketMQEvent",
    "DMS4RocketMQRecord",
    "DMS4RocketMQRecordMessage",
]