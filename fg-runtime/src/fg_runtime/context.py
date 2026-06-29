"""Context implementation for the FunctionGraph Python runtime."""

import json
import time

from .logger import Logger


def _parse_json(raw_value=None):
    try:
        return json.loads(raw_value)
    except (TypeError, ValueError):
        return {}


class Context:
    """Execution context exposed to FunctionGraph handlers."""

    def __init__(self, options=None):
        options = options or {}
        func_env = options.get("funcEnv") or {}

        self.function_name = func_env.get("RUNTIME_FUNC_NAME") or ""
        self.package = func_env.get("RUNTIME_PACKAGE") or ""
        self.project_id = func_env.get("RUNTIME_PROJECT_ID") or ""
        self.function_version = func_env.get("RUNTIME_FUNC_VERSION") or ""
        self.memory = func_env.get("RUNTIME_MEMORY") or "0"
        self.cpu = func_env.get("RUNTIME_CPU") or "0"
        self.user_data = _parse_json(func_env.get("RUNTIME_USERDATA")) or {}
        timeout = func_env.get("RUNTIME_TIMEOUT")
        self.timeout = timeout * 1000 if timeout else 3000
        self.start_time = int(time.time() * 1000)
        self.request_id = options.get("requestID") or ""
        self.access_key = options.get("accessKey") or ""
        self.secret_key = options.get("secretKey") or ""
        self.security_access_key = options.get("securityAccessKey") or ""
        self.security_secret_key = options.get("securitySecretKey") or ""
        self.auth_token = options.get("authToken") or ""
        self.security_token = options.get("securityToken") or ""
        self.logger = Logger(self.request_id, options.get("invokeID"))
        self.invoke_id = options.get("invokeID")
        self.invoke_property = None
        self.from_task = False
        self.instance_id = None
        self.state = None
        self.trace_id = self.request_id
        self.alias = options.get("alias") or ""
        self.workflow_id = options.get("workflowID") or ""
        self.workflow_run_id = options.get("workflowRunID") or ""
        self.workflow_state_id = options.get("workflowStateID") or ""

    def get_alias(self):
        return self.alias

    def get_project_id(self):
        return self.project_id

    def get_package(self):
        return self.package

    def get_function_name(self):
        return self.function_name

    def get_version(self):
        return self.function_version

    def get_memory_size(self):
        return self.memory

    def get_cpu_number(self):
        return self.cpu

    def get_running_time_in_seconds(self):
        return self.timeout

    def get_user_data(self, key):
        return self.user_data.get(key)

    def get_request_id(self):
        return self.request_id

    def get_remaining_time_in_milli_seconds(self):
        now = int(time.time() * 1000)
        return self.timeout + self.start_time - now

    def get_access_key(self):
        return self.access_key

    def get_secret_key(self):
        return self.secret_key

    def get_security_access_key(self):
        return self.security_access_key

    def get_security_secret_key(self):
        return self.security_secret_key

    def get_workflow_id(self):
        return self.workflow_id

    def get_workflow_run_id(self):
        return self.workflow_run_id

    def get_workflow_state_id(self):
        return self.workflow_state_id

    def get_token(self):
        return self.auth_token

    def get_security_token(self):
        return self.security_token

    def get_logger(self):
        return self.logger


__all__ = ["Context"]