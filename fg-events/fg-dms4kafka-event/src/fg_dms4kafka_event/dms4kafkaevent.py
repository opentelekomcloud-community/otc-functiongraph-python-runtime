"""DMS Kafka event classes for FunctionGraph."""


class DMS4KafkaEvent:
    """Represents a DMS4Kafka event for FunctionGraph."""

    def __init__(self, event):
        self._event = event or {}
        self._records = [DMS4KafkaRecord(record) for record in self._event.get("records") or []]

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
        return self._records

    def to_json(self):
        return self._event


class DMS4KafkaRecord:
    """Represents a topic record in a DMS4Kafka event."""

    def __init__(self, record):
        self._record = record or {}
        self._messages = [
            DMS4KafkaRecordMessage(message) for message in self._record.get("messages") or []
        ]

    def get_topic_id(self):
        return self._record.get("topic_id") or ""

    def get_messages(self):
        return self._messages

    def to_json(self):
        return self._record


class DMS4KafkaRecordMessage:
    """Represents a single Kafka message in a DMS4Kafka record."""

    def __init__(self, record):
        self._record = record or {}

    def get_message(self):
        if isinstance(self._record, str):
            return self._record
        return self._record.get("message") or ""

    def to_json(self):
        return self._record


__all__ = ["DMS4KafkaEvent", "DMS4KafkaRecord", "DMS4KafkaRecordMessage"]