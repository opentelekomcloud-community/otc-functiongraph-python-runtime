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

        self.assertEqual(context.getFunctionName(), "demo-function")
        self.assertEqual(context.getPackage(), "default")
        self.assertEqual(context.getProjectID(), "project-1")
        self.assertEqual(context.getVersion(), "latest")
        self.assertEqual(context.getMemorySize(), "512")
        self.assertEqual(context.getCPUNumber(), "1")
        self.assertEqual(context.getUserData("key"), "value")
        self.assertEqual(context.getRequestID(), "request-1")
        self.assertEqual(context.getAccessKey(), "ak")
        self.assertEqual(context.getSecretKey(), "sk")
        self.assertEqual(context.getSecurityAccessKey(), "sak")
        self.assertEqual(context.getSecuritySecretKey(), "ssk")
        self.assertEqual(context.getToken(), "auth")
        self.assertEqual(context.getSecurityToken(), "security")
        self.assertEqual(context.getAlias(), "prod")
        self.assertEqual(context.getWorkflowID(), "workflow-1")
        self.assertEqual(context.getWorkflowRunID(), "workflow-run-1")
        self.assertEqual(context.getWorkflowStateID(), "workflow-state-1")
        self.assertIsInstance(context.getLogger(), Logger)
        self.assertEqual(context.getRunningTimeInSeconds(), 10000)
        self.assertLessEqual(context.getRemainingTimeInMilliSeconds(), 10000)

    def test_context_defaults_when_optional_values_are_missing(self):
        context = Context({"funcEnv": {"RUNTIME_USERDATA": "not-json"}})

        self.assertEqual(context.getFunctionName(), "")
        self.assertEqual(context.getPackage(), "")
        self.assertEqual(context.getProjectID(), "")
        self.assertEqual(context.getVersion(), "")
        self.assertEqual(context.getMemorySize(), "0")
        self.assertEqual(context.getCPUNumber(), "0")
        self.assertIsNone(context.getUserData("missing"))
        self.assertEqual(context.getRequestID(), "")
        self.assertEqual(context.getRunningTimeInSeconds(), 3000)
        self.assertIsInstance(context.getLogger(), Logger)


if __name__ == "__main__":
    unittest.main()