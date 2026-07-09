"""Context implementation for the FunctionGraph Python runtime."""

import json
import time

from .fn_runtime_log import acquire_function_logger


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
        #self.logger = Logger(self.request_id, options.get("invokeID"))
        self.logger = acquire_function_logger(self.request_id, options.get("invokeID"))
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

    def getAlias(self):
        """Method getAlias"""
        return self.alias

    def getProjectID(self):
        """Method getProjectID"""
        return self.project_id

    def getPackage(self):
        """Method getPackage"""
        return self.package

    def getFunctionName(self):
        """Method getFunctionName"""
        return self.function_name

    def getVersion(self):
        """Method getVersion"""
        return self.function_version

    # Get the memory size distributed the running function
    def getMemorySize(self):
        """Method getMemorySize"""
        return self.memory

    # Get the number of cpu distributed to the running function the cpu
    # number scale by millicores, one cpu cores equals 1000 millicores. In
    # function stage runtime, every function have base of 200 millicores,
    # and increased by memory size distributed to function. the offset is
    # about Memory Size(M)/128 * 100
    def getCPUNumber(self):
        """Method getCPUNumber"""
        return self.cpu

    # Gets the time distributed to the running of the function, when exceed
    # the specified time, the running of the function would be stopped by force
    def getRunningTimeInSeconds(self):
        """Method getRunningTimeInSeconds"""
        return self.timeout

    # Gets the user data,which saved in a map
    def getUserData(self, key):
        """Method getUserData"""
        return self.user_data.get(key)

    def getRequestID(self):
        """Method getRequestID"""
        return self.request_id

    # Gets the time remaining for this execution in milliseconds
    # Returns time before task is killed
    def getRemainingTimeInMilliSeconds(self):
        """Method getRemainingTimeInMilliSeconds"""
        now = int(time.time() * 1000)
        return self.timeout + self.start_time - now

    # Gets the Access key information of the tenant
    def getAccessKey(self):
        """Method getAccessKey"""
        return self.access_key

    # Gets the Secret Key information of the tenant
    def getSecretKey(self):
        """Method getSecretKey"""
        return self.secret_key

    # Gets the Security Access key information of the tenant
    def getSecurityAccessKey(self):
        """Method getSecurityAccessKey"""
        return self.security_access_key

    # Gets the Security Secret Key information of the tenant
    def getSecuritySecretKey(self):
        """Method getSecuritySecretKey"""
        return self.security_secret_key

    # Gets the workflow id information of the tenant
    def getWorkflowID(self):
        """Method getWorkflowID"""
        return self.workflow_id

    # Gets the workflow run id information of the tenant
    def getWorkflowRunID(self):
        """Method getWorkflowRunID"""
        return self.workflow_run_id

    # Gets the workflow state id information of the tenant
    def getWorkflowStateID(self):
        """Method getWorkflowStateID"""
        return self.workflow_state_id

    def getToken(self):
        """Method getToken"""
        return self.auth_token

    def getSecurityToken(self):
        """Method getSecurityToken"""
        return self.security_token

    # Gets the logger for user to log out in standard output, The Logger
    # interface must be provided in SDK
    def getLogger(self):
        """Method getLogger"""
        return self.logger

    def set_state(self, state):
        """Method set_state"""
        self.state = state

    def get_state(self):
        """Method get_state"""
        return self.state

    def set_instance_id(self, instance_id):
        """Method set_instance_id"""
        self.instance_id = instance_id

    def get_instance_id(self):
        """Method get_instance_id"""
        return self.instance_id

    def get_invoke_id(self):
        """Method get_invoke_id"""
        return self.invoke_id

    def get_trace_id(self):
        """Method get_trace_id"""
        return self.request_id

    def get_invoke_property(self):
        """Method get_invoke_property"""
        return self.invoke_property

__all__ = ["Context"]