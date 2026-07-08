import sys
import unittest
from pathlib import Path

# fg-runtime and fg-apig-event sources
_ROOT = Path(__file__).resolve().parents[3]
# sys.path.insert(0, str(_ROOT / "fg-runtime" / "src"))
# sys.path.insert(0, str(_ROOT / "fg-events" / "fg-apig-event" / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fg_runtime import Context
from index import handler


def _make_context(function_name="scratch-event-apig"):
    return Context(
        {
            "funcEnv": {
                "RUNTIME_FUNC_NAME": function_name,
                "RUNTIME_PACKAGE": "default",
                "RUNTIME_PROJECT_ID": "project-1",
                "RUNTIME_FUNC_VERSION": "latest",
                "RUNTIME_MEMORY": "256",
                "RUNTIME_CPU": "1",
                "RUNTIME_USERDATA": "{}",
                "RUNTIME_TIMEOUT": 30,
            },
            "requestID": "test-request-1",
            "invokeID": "test-invoke-1",
        }
    )


def _make_event(response_type=None, body="", is_base64_encoded=False):
    event = {
        "requestContext": {
            "requestId": "a31d3d70415214292fa8b2cade9b4538",
            "apiId": "caf65eeb83a44b98a6264626007a73d4",
            "stage": "RELEASE",
        },
        "httpMethod": "GET",
        "path": "/test",
        "headers": {"accept": "text/html"},
        "pathParameters": {},
        "queryStringParameters": {},
        "body": body,
        "isBase64Encoded": is_base64_encoded,
    }
    if response_type is not None:
        event["queryStringParameters"]["responseType"] = response_type
    return event


class HandlerTests(unittest.TestCase):
    def test_returns_html_response_when_response_type_is_html(self):
        event = _make_event(response_type="html")
        context = _make_context()

        result = handler(event, context)

        self.assertEqual(result.status_code, 200)
        self.assertIn("Welcome to use FunctionGraph", result.get_body())
        self.assertEqual(
            result.headers.get("Content-Type"), "text/html; charset=utf-8"
        )

    def test_returns_json_response_when_response_type_is_json(self):
        import json

        payload = json.dumps({"hello": "world"})
        event = _make_event(response_type="json", body=payload)
        context = _make_context()

        result = handler(event, context)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            result.headers.get("Content-Type"), "application/json"
        )
        body = result.get_body()
        parsed = json.loads(body) if isinstance(body, str) else body
        self.assertEqual(parsed.get("hello"), "world")

    def test_returns_fallback_html_when_no_response_type(self):
        event = _make_event()
        context = _make_context()

        result = handler(event, context)

        self.assertEqual(result.status_code, 200)
        self.assertIn("responseType", result.get_body())

    def test_returns_error_body_for_invalid_json_with_json_response_type(self):
        import json

        event = _make_event(response_type="json", body="not-valid-json")
        context = _make_context()

        result = handler(event, context)

        self.assertEqual(result.status_code, 200)
        body = result.get_body()
        parsed = json.loads(body) if isinstance(body, str) else body
        self.assertIn("error", parsed)

    def test_context_function_name_is_accessible(self):
        event = _make_event(response_type="html")
        context = _make_context(function_name="my-apig-fn")

        # handler uses context.getFunctionName() — ensure it doesn't raise
        result = handler(event, context)

        self.assertIsNotNone(result)
        self.assertEqual(context.getFunctionName(), "my-apig-fn")


if __name__ == "__main__":
    unittest.main()
