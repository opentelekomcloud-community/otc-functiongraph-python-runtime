import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fg_smn_event import SMNEvent


class SMNEventTests(unittest.TestCase):
    def test_nested_wrappers_return_event_values(self):
        payload = {
            "record": [
                {
                    "event_subscription_urn": "urn:smn:subscription:1",
                    "event_source": "smn",
                    "smn": {
                        "topic_urn": "urn:smn:topic:1",
                        "timestamp": "2024-01-01T00:00:00Z",
                        "message_attributes": {"severity": "info"},
                        "message": "hello",
                        "type": "Notification",
                        "message_id": "message-1",
                        "subject": "demo-subject",
                    },
                }
            ],
            "functionname": "demo-function",
            "requestId": "request-1",
            "timestamp": "2024-01-01T00:00:01Z",
        }

        event = SMNEvent(payload)
        record = event.get_records()[0]
        body = record.get_smn_body()

        self.assertEqual(len(event.get_records()), 1)
        self.assertEqual(event.get_function_name(), "demo-function")
        self.assertEqual(event.get_request_id(), "request-1")
        self.assertEqual(event.get_timestamp(), "2024-01-01T00:00:01Z")
        self.assertEqual(record.get_event_subscription_urn(), "urn:smn:subscription:1")
        self.assertEqual(record.get_event_source(), "smn")
        self.assertEqual(body.get_topic_urn(), "urn:smn:topic:1")
        self.assertEqual(body.get_timestamp(), "2024-01-01T00:00:00Z")
        self.assertEqual(body.get_message_attributes(), {"severity": "info"})
        self.assertEqual(body.get_message(), "hello")
        self.assertEqual(body.get_type(), "Notification")
        self.assertEqual(body.get_message_id(), "message-1")
        self.assertEqual(body.get_subject(), "demo-subject")

    def test_missing_values_fall_back_to_defaults(self):
        event = SMNEvent({"record": [{}]})
        record = event.get_records()[0]
        body = record.get_smn_body()

        self.assertEqual(event.get_function_name(), "")
        self.assertEqual(event.get_request_id(), "")
        self.assertEqual(event.get_timestamp(), "")
        self.assertEqual(record.get_event_subscription_urn(), "")
        self.assertEqual(record.get_event_source(), "")
        self.assertEqual(body.get_topic_urn(), "")
        self.assertEqual(body.get_timestamp(), "")
        self.assertIsNone(body.get_message_attributes())
        self.assertEqual(body.get_message(), "")
        self.assertEqual(body.get_type(), "")
        self.assertEqual(body.get_message_id(), "")
        self.assertEqual(body.get_subject(), "")

    def test_to_json_returns_original_wrapped_payloads(self):
        payload = {
            "record": [
                {
                    "smn": {
                        "message": "hello",
                    }
                }
            ]
        }

        event = SMNEvent(payload)
        record = event.get_records()[0]

        self.assertIs(event.to_json(), payload)
        self.assertIs(record.to_json(), payload["record"][0])
        self.assertIs(record.get_smn_body().to_json(), payload["record"][0]["smn"])


if __name__ == "__main__":
    unittest.main()