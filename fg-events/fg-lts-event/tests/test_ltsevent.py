import base64
import json
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fg_lts_event import LTSEvent


def _encode_payload(payload):
    return base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")


class LTSEventTests(unittest.TestCase):
    def test_get_raw_data_returns_nested_lts_data(self):
        event = LTSEvent({"lts": {"data": "payload"}})

        self.assertEqual(event.get_raw_data(), "payload")

    def test_get_data_decodes_base64_utf8_payload(self):
        raw_data = base64.b64encode(b'{"message":"ok"}').decode("utf-8")
        event = LTSEvent({"lts": {"data": raw_data}})

        self.assertEqual(event.get_data(), '{"message":"ok"}')

    def test_get_data_returns_empty_string_for_invalid_base64(self):
        event = LTSEvent({"lts": {"data": "not-base64"}})

        self.assertEqual(event.get_data(), "")

    def test_get_logs_returns_logs_from_decoded_json_payload(self):
        payload = {
            "logs": [
                {"message": "first", "timestamp": 1},
                {"message": "second", "timestamp": 2},
            ]
        }
        event = LTSEvent({"lts": {"data": _encode_payload(payload)}})

        self.assertEqual(event.get_logs(), payload["logs"])

    def test_get_logs_returns_empty_list_for_invalid_json_payload(self):
        raw_data = base64.b64encode(b"plain text").decode("utf-8")
        event = LTSEvent({"lts": {"data": raw_data}})

        self.assertEqual(event.get_logs(), [])

    def test_to_json_returns_original_event(self):
        payload = {"lts": {"data": _encode_payload({"logs": []})}}
        event = LTSEvent(payload)

        self.assertIs(event.to_json(), payload)


if __name__ == "__main__":
    unittest.main()