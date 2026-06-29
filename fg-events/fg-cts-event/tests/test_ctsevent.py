import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fg_cts_event import CTSEvent


class CTSEventTests(unittest.TestCase):
    def test_getters_return_values_from_nested_cts_payload(self):
        payload = {
            "cts": {
                "time": 1660927593570,
                "request": {"method": "POST"},
                "response": {"status": "ok"},
                "service_type": "IAM",
                "event_type": "management",
                "project_id": "project-1",
                "resource_type": "user",
                "resource_account_id": "account-2",
                "read_only": True,
                "tracker_name": "system",
                "operation_id": "operation-1",
                "resource_name": "demo-user",
                "resource_id": "resource-1",
                "source_ip": "127.0.0.1",
                "domain_id": "domain-1",
                "trace_name": "createUser",
                "trace_status": "normal",
                "trace_rating": "normal",
                "trace_type": "ApiCall",
                "api_version": "v3",
                "message": "done",
                "record_time": "2024-01-01T00:00:00Z",
                "trace_id": "trace-1",
                "code": "200",
                "request_id": "request-1",
                "location_info": {"region": "eu-de"},
                "endpoint": "iam.eu-de.otc.t-systems.com",
                "resource_url": "/v3/users",
                "enterprise_project_id": "ep-1",
                "user_agent": "curl/8.0",
                "content_length": 128,
                "total_time": 42,
                "user": {
                    "type": "IAMUser",
                    "principal_id": "principal-1",
                    "principal_urn": "iam::account:user:demo",
                    "account_id": "account-1",
                    "access_key_id": "ak-1",
                    "id": "user-1",
                    "name": "demo",
                    "domain": {"id": "domain-1", "name": "demo-domain"},
                    "user_name": "demo",
                    "principal_is_root_user": False,
                    "invoked_by": ["service.console"],
                    "session_context": {
                        "attributes": {
                            "created_at": "2024-01-01T00:00:00Z",
                            "mfa_authenticated": True,
                        }
                    },
                    "OriginUser": "origin-demo",
                },
            }
        }

        event = CTSEvent(payload)
        user = event.get_user()
        domain = user.get_domain()
        session_attributes = user.get_session_context().get_attributes()

        self.assertEqual(event.get_time(), 1660927593570)
        self.assertEqual(event.get_request(), {"method": "POST"})
        self.assertEqual(event.get_response(), {"status": "ok"})
        self.assertEqual(event.get_service_type(), "IAM")
        self.assertEqual(event.get_event_type(), "management")
        self.assertEqual(event.get_project_id(), "project-1")
        self.assertEqual(event.get_resource_type(), "user")
        self.assertEqual(event.get_resource_account_id(), "account-2")
        self.assertTrue(event.get_read_only())
        self.assertEqual(event.get_tracker_name(), "system")
        self.assertEqual(event.get_operation_id(), "operation-1")
        self.assertEqual(event.get_resource_name(), "demo-user")
        self.assertEqual(event.get_resource_id(), "resource-1")
        self.assertEqual(event.get_source_ip(), "127.0.0.1")
        self.assertEqual(event.get_domain_id(), "domain-1")
        self.assertEqual(event.get_trace_name(), "createUser")
        self.assertEqual(event.get_trace_status(), "normal")
        self.assertEqual(event.get_trace_rating(), "normal")
        self.assertEqual(event.get_trace_type(), "ApiCall")
        self.assertEqual(event.get_api_version(), "v3")
        self.assertEqual(event.get_message(), "done")
        self.assertEqual(event.get_record_time(), "2024-01-01T00:00:00Z")
        self.assertEqual(event.get_trace_id(), "trace-1")
        self.assertEqual(event.get_code(), "200")
        self.assertEqual(event.get_request_id(), "request-1")
        self.assertEqual(event.get_location_info(), {"region": "eu-de"})
        self.assertEqual(event.get_endpoint(), "iam.eu-de.otc.t-systems.com")
        self.assertEqual(event.get_resource_url(), "/v3/users")
        self.assertEqual(event.get_enterprise_project_id(), "ep-1")
        self.assertEqual(event.get_user_agent(), "curl/8.0")
        self.assertEqual(event.get_content_length(), 128)
        self.assertEqual(event.get_total_time(), 42)
        self.assertEqual(user.get_type(), "IAMUser")
        self.assertEqual(user.get_principal_id(), "principal-1")
        self.assertEqual(user.get_principal_urn(), "iam::account:user:demo")
        self.assertEqual(user.get_account_id(), "account-1")
        self.assertEqual(user.get_access_key_id(), "ak-1")
        self.assertEqual(user.get_id(), "user-1")
        self.assertEqual(user.get_name(), "demo")
        self.assertEqual(user.get_user_name(), "demo")
        self.assertFalse(user.get_principal_is_root_user())
        self.assertEqual(user.get_invoked_by(), ["service.console"])
        self.assertEqual(user.get_origin_user(), "origin-demo")
        self.assertEqual(domain.get_id(), "domain-1")
        self.assertEqual(domain.get_name(), "demo-domain")
        self.assertEqual(session_attributes.get_created_at(), "2024-01-01T00:00:00Z")
        self.assertTrue(session_attributes.get_mfa_authenticated())

    def test_missing_values_fall_back_to_defaults(self):
        event = CTSEvent({})
        user = event.get_user()
        session_attributes = user.get_session_context().get_attributes()

        self.assertEqual(event.get_time(), 0)
        self.assertEqual(event.get_service_type(), "")
        self.assertFalse(event.get_read_only())
        self.assertEqual(event.get_location_info(), {})
        self.assertEqual(event.get_content_length(), 0)
        self.assertEqual(event.get_total_time(), 0)
        self.assertEqual(user.get_name(), "")
        self.assertEqual(user.get_invoked_by(), [])
        self.assertEqual(session_attributes.get_mfa_authenticated(), "")

    def test_to_json_returns_inner_cts_payload(self):
        payload = {"cts": {"trace_id": "trace-1"}}
        event = CTSEvent(payload)

        self.assertIs(event.to_json(), payload["cts"])


if __name__ == "__main__":
    unittest.main()