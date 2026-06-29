import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fg_runtime import Context, Logger


class ContextTests(unittest.TestCase):
    def test_context_exposes_runtime_values(self):
        context = Context(
            {
                "funcEnv": {
                    "RUNTIME_FUNC_NAME": "demo-function",
                    "RUNTIME_PACKAGE": "default",
                    "RUNTIME_PROJECT_ID": "project-1",
                    "RUNTIME_FUNC_VERSION": "latest",
                    "RUNTIME_MEMORY": "512",
                    "RUNTIME_CPU": "1",
                    "RUNTIME_USERDATA": '{"key": "value"}',
                    "RUNTIME_TIMEOUT": 10,
                },
                "requestID": "request-1",
                "accessKey": "ak",
                "secretKey": "sk",
                "securityAccessKey": "sak",
                "securitySecretKey": "ssk",
                "authToken": "auth",
                "securityToken": "security",
                "invokeID": "invoke-1",
                "alias": "prod",
                "workflowID": "workflow-1",
                "workflowRunID": "workflow-run-1",
                "workflowStateID": "workflow-state-1",
            }
        )

        self.assertEqual(context.get_function_name(), "demo-function")
        self.assertEqual(context.get_package(), "default")
        self.assertEqual(context.get_project_id(), "project-1")
        self.assertEqual(context.get_version(), "latest")
        self.assertEqual(context.get_memory_size(), "512")
        self.assertEqual(context.get_cpu_number(), "1")
        self.assertEqual(context.get_user_data("key"), "value")
        self.assertEqual(context.get_request_id(), "request-1")
        self.assertEqual(context.get_access_key(), "ak")
        self.assertEqual(context.get_secret_key(), "sk")
        self.assertEqual(context.get_security_access_key(), "sak")
        self.assertEqual(context.get_security_secret_key(), "ssk")
        self.assertEqual(context.get_token(), "auth")
        self.assertEqual(context.get_security_token(), "security")
        self.assertEqual(context.get_alias(), "prod")
        self.assertEqual(context.get_workflow_id(), "workflow-1")
        self.assertEqual(context.get_workflow_run_id(), "workflow-run-1")
        self.assertEqual(context.get_workflow_state_id(), "workflow-state-1")
        self.assertIsInstance(context.get_logger(), Logger)
        self.assertEqual(context.get_running_time_in_seconds(), 10000)
        self.assertLessEqual(context.get_remaining_time_in_milli_seconds(), 10000)

    def test_context_defaults_when_optional_values_are_missing(self):
        context = Context({"funcEnv": {"RUNTIME_USERDATA": "not-json"}})

        self.assertEqual(context.get_function_name(), "")
        self.assertEqual(context.get_package(), "")
        self.assertEqual(context.get_project_id(), "")
        self.assertEqual(context.get_version(), "")
        self.assertEqual(context.get_memory_size(), "0")
        self.assertEqual(context.get_cpu_number(), "0")
        self.assertIsNone(context.get_user_data("missing"))
        self.assertEqual(context.get_request_id(), "")
        self.assertEqual(context.get_running_time_in_seconds(), 3000)
        self.assertIsInstance(context.get_logger(), Logger)


if __name__ == "__main__":
    unittest.main()