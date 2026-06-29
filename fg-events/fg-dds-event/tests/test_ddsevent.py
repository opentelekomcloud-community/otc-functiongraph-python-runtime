import json
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fg_dds_event import DDSEvent


class DDSEventTests(unittest.TestCase):
    def test_record_access_and_nested_dds_values(self):
        payload = {
            "records": [
                {
                    "event_source": "DDS",
                    "event_version": "1.0",
                    "event_name": "insert",
                    "event_source_ip": "127.0.0.1",
                    "region": "eu-de",
                    "dds": {
                        "size_bytes": 128,
                        "token": json.dumps({"resume_token": "abc"}),
                        "full_document": json.dumps({"_id": 1, "name": "demo"}),
                        "ns": json.dumps({"db": "test", "coll": "items"}),
                    },
                }
            ]
        }

        event = DDSEvent(payload)
        record = event.get_record(0)
        dds = record.get_dds()

        self.assertEqual(len(event.get_records()), 1)
        self.assertEqual(record.get_event_source(), "DDS")
        self.assertEqual(record.get_event_version(), "1.0")
        self.assertEqual(record.get_event_name(), "insert")
        self.assertEqual(record.get_event_source_ip(), "127.0.0.1")
        self.assertEqual(record.get_region(), "eu-de")
        self.assertEqual(dds.get_size_bytes(), 128)
        self.assertEqual(dds.get_token_raw(), '{"resume_token": "abc"}')
        self.assertEqual(dds.get_token(), {"resume_token": "abc"})
        self.assertEqual(dds.get_full_document_raw(), '{"_id": 1, "name": "demo"}')
        self.assertEqual(dds.get_full_document(), {"_id": 1, "name": "demo"})
        self.assertEqual(dds.get_ns_raw(), '{"db": "test", "coll": "items"}')
        self.assertEqual(dds.get_ns(), {"db": "test", "coll": "items"})

    def test_get_record_returns_none_when_index_is_out_of_range(self):
        event = DDSEvent({"records": []})

        self.assertIsNone(event.get_record(0))

    def test_json_parsing_helpers_accept_existing_objects(self):
        event = DDSEvent(
            {
                "records": [
                    {
                        "dds": {
                            "token": {"resume_token": "abc"},
                            "full_document": {"_id": 1},
                            "ns": {"db": "test"},
                        }
                    }
                ]
            }
        )
        dds = event.get_record(0).get_dds()

        self.assertEqual(dds.get_token(), {"resume_token": "abc"})
        self.assertEqual(dds.get_full_document(), {"_id": 1})
        self.assertEqual(dds.get_ns(), {"db": "test"})

    def test_invalid_json_values_fall_back_to_empty_dicts(self):
        event = DDSEvent(
            {
                "records": [
                    {
                        "dds": {
                            "token": "not-json",
                            "full_document": "also-not-json",
                            "ns": "broken",
                        }
                    }
                ]
            }
        )
        dds = event.get_record(0).get_dds()

        self.assertEqual(dds.get_token(), {})
        self.assertEqual(dds.get_full_document(), {})
        self.assertEqual(dds.get_ns(), {})

    def test_to_json_returns_original_wrapped_payloads(self):
        payload = {"records": [{"dds": {"size_bytes": 1}}]}
        event = DDSEvent(payload)
        record = event.get_record(0)

        self.assertIs(event.to_json(), payload)
        self.assertIs(record.to_json(), payload["records"][0])
        self.assertIs(record.get_dds().to_json(), payload["records"][0]["dds"])


if __name__ == "__main__":
    unittest.main()