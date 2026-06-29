import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fg_dms4rocketmq_event import DMS4RocketMQEvent


class DMS4RocketMQEventTests(unittest.TestCase):
    def test_nested_wrappers_return_event_values(self):
        payload = {
            "event_version": "1.0",
            "event_time": "2024-01-01T00:00:00Z",
            "region": "eu-de",
            "trigger_type": "ROCKETMQ",
            "instance_id": "instance-1",
            "records": [
                {
                    "topic_id": "topic-1",
                    "messages": [
                        "plain-message",
                        {"message": "object-message"},
                    ],
                }
            ],
        }

        event = DMS4RocketMQEvent(payload)
        records = event.get_records()
        record = records[0]
        messages = record.get_messages()

        self.assertEqual(event.get_event_version(), "1.0")
        self.assertEqual(event.get_event_time(), "2024-01-01T00:00:00Z")
        self.assertEqual(event.get_region(), "eu-de")
        self.assertEqual(event.get_trigger_type(), "ROCKETMQ")
        self.assertEqual(event.get_instance_id(), "instance-1")
        self.assertEqual(len(records), 1)
        self.assertEqual(record.get_topic_id(), "topic-1")
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0].get_message(), "plain-message")
        self.assertEqual(messages[1].get_message(), "object-message")

    def test_get_records_returns_new_wrappers_each_call(self):
        event = DMS4RocketMQEvent({"records": [{"topic_id": "topic-1"}]})

        first_records = event.get_records()
        second_records = event.get_records()

        self.assertIsNot(first_records, second_records)
        self.assertIsNot(first_records[0], second_records[0])
        self.assertEqual(first_records[0].get_topic_id(), second_records[0].get_topic_id())

    def test_missing_values_fall_back_to_defaults(self):
        event = DMS4RocketMQEvent({"records": [{}]})
        record = event.get_records()[0]

        self.assertEqual(event.get_event_version(), "")
        self.assertEqual(event.get_event_time(), "")
        self.assertEqual(event.get_region(), "")
        self.assertEqual(event.get_trigger_type(), "")
        self.assertEqual(event.get_instance_id(), "")
        self.assertEqual(record.get_topic_id(), "")
        self.assertEqual(record.get_messages(), [])

    def test_object_message_without_message_field_returns_empty_string(self):
        event = DMS4RocketMQEvent({"records": [{"messages": [{}]}]})

        message = event.get_records()[0].get_messages()[0]

        self.assertEqual(message.get_message(), "")

    def test_to_json_returns_original_wrapped_payloads(self):
        payload = {
            "records": [
                {
                    "messages": [
                        "plain-message",
                    ]
                }
            ]
        }

        event = DMS4RocketMQEvent(payload)
        record = event.get_records()[0]
        message = record.get_messages()[0]

        self.assertIs(event.to_json(), payload)
        self.assertIs(record.to_json(), payload["records"][0])
        self.assertIs(message.to_json(), payload["records"][0]["messages"][0])


if __name__ == "__main__":
    unittest.main()