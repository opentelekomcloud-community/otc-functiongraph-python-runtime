import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fg_obss3_event import OBSS3Event


class OBSS3EventTests(unittest.TestCase):
    def test_nested_wrappers_return_record_values(self):
        payload = {
            "Records": [
                {
                    "eventVersion": "2.1",
                    "eventTime": "2024-01-01T00:00:00.000Z",
                    "requestParameters": {"sourceIPAddress": "127.0.0.1"},
                    "s3": {
                        "configurationId": "config-1",
                        "object": {
                            "eTag": "etag-1",
                            "sequencer": "seq-1",
                            "key": "images/demo.png",
                            "size": 1024,
                        },
                        "bucket": {
                            "arn": "arn:aws:s3:::demo-bucket",
                            "name": "demo-bucket",
                            "ownerIdentity": {"PrincipalId": "owner-1"},
                        },
                    },
                    "awsRegion": "eu-de",
                    "eventName": "ObjectCreated:Post",
                    "userIdentity": {"principalId": "user-1"},
                }
            ]
        }

        event = OBSS3Event(payload)
        record = event.get_records()[0]
        request_parameters = record.get_request_parameters()
        s3_details = record.get_s3()
        s3_object = s3_details.get_object()
        bucket = s3_details.get_bucket()

        self.assertEqual(len(event.get_records()), 1)
        self.assertEqual(record.get_event_version(), "2.1")
        self.assertEqual(record.get_event_time(), "2024-01-01T00:00:00.000Z")
        self.assertEqual(request_parameters.get_source_ip_address(), "127.0.0.1")
        self.assertEqual(s3_details.get_configuration_id(), "config-1")
        self.assertEqual(s3_object.get_e_tag(), "etag-1")
        self.assertEqual(s3_object.get_sequencer(), "seq-1")
        self.assertEqual(s3_object.get_key(), "images/demo.png")
        self.assertEqual(s3_object.get_size(), 1024)
        self.assertEqual(bucket.get_arn(), "arn:aws:s3:::demo-bucket")
        self.assertEqual(bucket.get_name(), "demo-bucket")
        self.assertEqual(bucket.get_owner_identity().get_principal_id(), "owner-1")
        self.assertEqual(record.get_aws_region(), "eu-de")
        self.assertEqual(record.get_event_name(), "ObjectCreated:Post")
        self.assertEqual(record.get_user_identity().get_principal_id(), "user-1")

    def test_missing_values_fall_back_to_defaults(self):
        event = OBSS3Event({"Records": [{}]})
        record = event.get_records()[0]
        request_parameters = record.get_request_parameters()
        s3_details = record.get_s3()
        s3_object = s3_details.get_object()
        bucket = s3_details.get_bucket()

        self.assertEqual(record.get_event_version(), "")
        self.assertEqual(record.get_event_time(), "")
        self.assertEqual(request_parameters.get_source_ip_address(), "")
        self.assertEqual(s3_details.get_configuration_id(), "")
        self.assertEqual(s3_object.get_e_tag(), "")
        self.assertEqual(s3_object.get_sequencer(), "")
        self.assertEqual(s3_object.get_key(), "")
        self.assertEqual(s3_object.get_size(), 0)
        self.assertEqual(bucket.get_arn(), "")
        self.assertEqual(bucket.get_name(), "")
        self.assertEqual(bucket.get_owner_identity().get_principal_id(), "")
        self.assertEqual(record.get_aws_region(), "")
        self.assertEqual(record.get_event_name(), "")
        self.assertEqual(record.get_user_identity().get_principal_id(), "")

    def test_to_json_returns_original_wrapped_payloads(self):
        payload = {
            "Records": [
                {
                    "requestParameters": {"sourceIPAddress": "127.0.0.1"},
                    "s3": {
                        "object": {"key": "demo.txt"},
                        "bucket": {"ownerIdentity": {"PrincipalId": "owner-1"}},
                    },
                    "userIdentity": {"principalId": "user-1"},
                }
            ]
        }

        event = OBSS3Event(payload)
        record = event.get_records()[0]

        self.assertIs(event.to_json(), payload)
        self.assertIs(record.to_json(), payload["Records"][0])
        self.assertIs(record.get_request_parameters().to_json(), payload["Records"][0]["requestParameters"])
        self.assertIs(record.get_s3().to_json(), payload["Records"][0]["s3"])
        self.assertIs(record.get_s3().get_object().to_json(), payload["Records"][0]["s3"]["object"])
        self.assertIs(record.get_s3().get_bucket().to_json(), payload["Records"][0]["s3"]["bucket"])
        self.assertIs(
            record.get_s3().get_bucket().get_owner_identity().to_json(),
            payload["Records"][0]["s3"]["bucket"]["ownerIdentity"],
        )
        self.assertIs(record.get_user_identity().to_json(), payload["Records"][0]["userIdentity"])


if __name__ == "__main__":
    unittest.main()