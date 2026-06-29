"""SMN event classes for FunctionGraph."""


class SMNEvent:
    """Represents a Simple Message Notification event for FunctionGraph."""

    def __init__(self, event):
        self._event = event or {}
        self._records = [SMNRecord(record) for record in self._event.get("record") or []]

    def get_records(self):
        return self._records

    def get_function_name(self):
        return self._event.get("functionname") or ""

    def get_request_id(self):
        return self._event.get("requestId") or ""

    def get_timestamp(self):
        return self._event.get("timestamp") or ""

    def to_json(self):
        return self._event


class SMNRecord:
    """Represents a single SMN event record."""

    def __init__(self, record):
        self._record = record or {}

    def get_event_subscription_urn(self):
        return self._record.get("event_subscription_urn") or ""

    def get_event_source(self):
        return self._record.get("event_source") or ""

    def get_smn_body(self):
        return SMNBody(self._record.get("smn"))

    def to_json(self):
        return self._record


class SMNBody:
    """Represents the SMN message body in a record."""

    def __init__(self, smn):
        self._smn = smn or {}

    def get_topic_urn(self):
        return self._smn.get("topic_urn") or ""

    def get_timestamp(self):
        return self._smn.get("timestamp") or ""

    def get_message_attributes(self):
        return self._smn.get("message_attributes")

    def get_message(self):
        return self._smn.get("message") or ""

    def get_type(self):
        return self._smn.get("type") or ""

    def get_message_id(self):
        return self._smn.get("message_id") or ""

    def get_subject(self):
        return self._smn.get("subject") or ""

    def to_json(self):
        return self._smn


__all__ = ["SMNEvent", "SMNRecord", "SMNBody"]