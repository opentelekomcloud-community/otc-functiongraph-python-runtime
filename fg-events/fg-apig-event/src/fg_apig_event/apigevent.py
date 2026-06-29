"""
APIGEvent, APIGRequestContext, and APIGResponse classes for FunctionGraph API Gateway events.
"""

import json
import base64


class APIGEvent:
    """
    Represents an API Gateway event for FunctionGraph.
    
    Attributes:
        body (str): The request body
        isBase64Encoded (bool): Whether the body is base64 encoded
        requestContext (dict): Request context information
        queryStringParameters (dict): Query string parameters
        httpMethod (str): HTTP method
        pathParameters (dict): Path parameters
        headers (dict): Request headers
        path (str): Request path
    """

    def __init__(self, event):
        """
        Initialize APIGEvent.
        
        Args:
            event (dict): The API Gateway event data
        """
        self._event = event or {}

    def get_body(self):
        """
        Returns the decoded request body.
        
        Returns:
            str: Body content in plain text
        """
        body = self._event.get("body")
        if self._event.get("isBase64Encoded"):
            if not isinstance(body, str) or len(body) == 0:
                return ""

            try:
                decoded_bytes = base64.b64decode(body)
                return decoded_bytes.decode("utf-8")
            except Exception:
                return ""

        return body or ""

    def get_raw_body(self):
        """
        Returns the raw request body.
        
        Returns:
            str: Body content as received
        """
        return self._event.get("body") or ""

    def get_request_context(self):
        """
        Returns the request context.
        
        Returns:
            APIGRequestContext: The request context object
        """
        return APIGRequestContext(self._event.get("requestContext"))

    def get_request_context_value(self, key):
        """
        Get a value from the request context by key.
        
        Args:
            key (str): The key to retrieve
            
        Returns:
            str: The value or empty string if not found
        """
        request_context = self.get_request_context()
        param_value = request_context.get_value(key) or request_context.get_value(key.lower())
        return param_value or ""

    def get_query_string_parameters(self):
        """
        Returns the query string parameters.
        
        Returns:
            dict: Query string parameters
        """
        return self._event.get("queryStringParameters") or {}

    def get_query_string_parameter(self, param_name):
        """
        Get a query string parameter by name.
        
        Args:
            param_name (str): The parameter name
            
        Returns:
            str: The parameter value or empty string if not found
        """
        params = self.get_query_string_parameters()
        param_value = params.get(param_name) or params.get(param_name.lower())
        return param_value or ""

    def get_http_method(self):
        """
        Returns the HTTP method.
        
        Returns:
            str: The HTTP method
        """
        return self._event.get("httpMethod") or ""

    def get_path_parameters(self):
        """
        Returns the path parameters.
        
        Returns:
            dict: Path parameters
        """
        return self._event.get("pathParameters") or {}

    def get_path_parameter(self, param_name):
        """
        Get a path parameter by name.
        
        Args:
            param_name (str): The parameter name
            
        Returns:
            str: The parameter value or empty string if not found
        """
        params = self.get_path_parameters()
        param_value = params.get(param_name) or params.get(param_name.lower())
        return param_value or ""

    def get_headers(self):
        """
        Returns the request headers.
        
        Returns:
            dict: Request headers
        """
        return self._event.get("headers") or {}

    def get_header(self, header_name):
        """
        Get a header value by name.
        
        Args:
            header_name (str): The header name
            
        Returns:
            str: The header value or empty string if not found
        """
        headers = self.get_headers()
        header_value = headers.get(header_name) or headers.get(header_name.lower())
        return header_value or ""

    def get_path(self):
        """
        Returns the request path.
        
        Returns:
            str: The request path
        """
        return self._event.get("path") or ""

    def is_base64_encoded(self):
        """
        Returns whether the body is base64 encoded.
        
        Returns:
            bool: True if base64 encoded, False otherwise
        """
        return self._event.get("isBase64Encoded", False)

    def to_json(self):
        """
        Returns the event as a dictionary.
        
        Returns:
            dict: The raw event data
        """
        return self._event


class APIGRequestContext:
    """
    Represents the request context of an API Gateway event.
    
    Attributes:
        apiId (str): The API ID
        requestId (str): The request ID
        stage (str): The stage
    """

    def __init__(self, request_context):
        """
        Initialize APIGRequestContext.
        
        Args:
            request_context (dict): The request context data
        """
        self._request_context = request_context or {}

    def get_api_id(self):
        """
        Returns the API ID.
        
        Returns:
            str: The API ID
        """
        return self._request_context.get("apiId") or ""

    def get_request_id(self):
        """
        Returns the request ID.
        
        Returns:
            str: The request ID
        """
        return self._request_context.get("requestId") or ""

    def get_stage(self):
        """
        Returns the stage.
        
        Returns:
            str: The stage
        """
        return self._request_context.get("stage") or ""

    def get_value(self, key):
        """
        Get a value from the request context by key.
        
        Args:
            key (str): The key to retrieve
            
        Returns:
            str: The value or None if not found
        """
        return self._request_context.get(key)

    def to_json(self):
        """
        Returns the request context as a dictionary.
        
        Returns:
            dict: The raw request context data
        """
        return self._request_context


class APIGResponse:
    """
    Represents an API Gateway response for FunctionGraph.
    
    Attributes:
        statusCode (int): HTTP status code
        body (str): Response body
        headers (dict): Response headers
        isBase64Encoded (bool): Whether the body is base64 encoded
    """

    def __init__(self, status_code=200, body="", headers=None, is_base64_encoded=False):
        """
        Initialize APIGResponse.
        
        Args:
            status_code (int, optional): HTTP status code. Defaults to 200.
            body (str, optional): Response body. Defaults to "".
            headers (dict, optional): Response headers. Defaults to {}.
            is_base64_encoded (bool, optional): Whether body is base64 encoded. Defaults to False.
        """
        self.status_code = status_code
        self.body = body
        self.headers = headers or {}
        self.is_base64_encoded = is_base64_encoded

    @classmethod
    def from_json(cls, data):
        """
        Create an APIGResponse from a dictionary.
        
        Args:
            data (dict): Dictionary with response data
            
        Returns:
            APIGResponse: A new APIGResponse instance
        """
        return cls(
            status_code=data.get("statusCode", 200),
            body=data.get("body", ""),
            headers=data.get("headers", {}),
            is_base64_encoded=data.get("isBase64Encoded", False),
        )

    def set_status_code(self, status_code):
        """
        Set the HTTP status code.
        
        Args:
            status_code (int): The HTTP status code
        """
        self.status_code = status_code

    def set_body(self, body, is_base64_encoded=False):
        """
        Set the response body.
        
        Args:
            body (str or dict): The body content
            is_base64_encoded (bool, optional): Whether to encode as base64. Defaults to False.
        """
        self.is_base64_encoded = is_base64_encoded

        if is_base64_encoded:
            if isinstance(body, str):
                self.body = base64.b64encode(body.encode("utf-8")).decode("utf-8")
            else:
                json_str = json.dumps(body)
                self.body = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
        else:
            if isinstance(body, str):
                self.body = body
            else:
                self.body = json.dumps(body)

    def get_raw_body(self):
        """
        Returns the raw response body.
        
        Returns:
            str: The body as stored
        """
        return self.body

    def get_body(self):
        """
        Returns the decoded response body.
        
        Returns:
            str: The body content in plain text
        """
        if self.is_base64_encoded:
            decoded_bytes = base64.b64decode(self.body)
            return decoded_bytes.decode("utf-8")
        return self.body

    def get_body_parsed(self):
        """
        Returns the parsed response body as a Python object.
        
        Returns:
            dict or str or None: The parsed body content
        """
        if self.body is None:
            return None
        return json.loads(self.get_body())

    def to_json(self):
        """
        Returns the response as a dictionary.
        
        Returns:
            dict: The response data
        """
        return {
            "statusCode": self.status_code,
            "body": self.body,
            "headers": self.headers,
            "isBase64Encoded": self.is_base64_encoded,
        }


# Export classes for use in other modules
__all__ = ["APIGEvent", "APIGRequestContext", "APIGResponse"]
