"""CTS event classes for FunctionGraph."""


class CTSEvent:
    """Represents a CTS event for FunctionGraph."""

    def __init__(self, event):
        self._event = (event or {}).get("cts") or {}

    def get_time(self):
        return self._event.get("time") or 0

    def get_user(self):
        return CTSUserInfo(self._event.get("user"))

    def get_request(self):
        return self._event.get("request") or {}

    def get_response(self):
        return self._event.get("response") or {}

    def get_service_type(self):
        return self._event.get("service_type") or ""

    def get_event_type(self):
        return self._event.get("event_type") or ""

    def get_project_id(self):
        return self._event.get("project_id") or ""

    def get_resource_type(self):
        return self._event.get("resource_type") or ""

    def get_resource_account_id(self):
        return self._event.get("resource_account_id") or ""

    def get_read_only(self):
        return self._event.get("read_only") or False

    def get_tracker_name(self):
        return self._event.get("tracker_name") or ""

    def get_operation_id(self):
        return self._event.get("operation_id") or ""

    def get_resource_name(self):
        return self._event.get("resource_name") or ""

    def get_resource_id(self):
        return self._event.get("resource_id") or ""

    def get_source_ip(self):
        return self._event.get("source_ip") or ""

    def get_domain_id(self):
        return self._event.get("domain_id") or ""

    def get_trace_name(self):
        return self._event.get("trace_name") or ""

    def get_trace_status(self):
        return self._event.get("trace_status") or ""

    def get_trace_rating(self):
        return self._event.get("trace_rating") or ""

    def get_trace_type(self):
        return self._event.get("trace_type") or ""

    def get_api_version(self):
        return self._event.get("api_version") or ""

    def get_message(self):
        return self._event.get("message") or ""

    def get_record_time(self):
        return self._event.get("record_time") or ""

    def get_trace_id(self):
        return self._event.get("trace_id") or ""

    def get_code(self):
        return self._event.get("code") or ""

    def get_request_id(self):
        return self._event.get("request_id") or ""

    def get_location_info(self):
        return self._event.get("location_info") or {}

    def get_endpoint(self):
        return self._event.get("endpoint") or ""

    def get_resource_url(self):
        return self._event.get("resource_url") or ""

    def get_enterprise_project_id(self):
        return self._event.get("enterprise_project_id") or ""

    def get_user_agent(self):
        return self._event.get("user_agent") or ""

    def get_content_length(self):
        return self._event.get("content_length") or 0

    def get_total_time(self):
        return self._event.get("total_time") or 0

    def to_json(self):
        return self._event


class CTSBaseUserDomain:
    """Represents the domain information on a CTS user object."""

    def __init__(self, user_domain):
        self._user_domain = user_domain or {}

    def get_id(self):
        return self._user_domain.get("id") or ""

    def get_name(self):
        return self._user_domain.get("name") or ""

    def to_json(self):
        return self._user_domain


class CTSSessionContext:
    """Represents temporary security credential context on a CTS user."""

    def __init__(self, session_context):
        self._session_context = session_context or {}

    def get_attributes(self):
        return CTSSessionContextAttributes(self._session_context.get("attributes"))

    def to_json(self):
        return self._session_context


class CTSSessionContextAttributes:
    """Represents session attributes for a CTS user context."""

    def __init__(self, session_attributes):
        self._session_attributes = session_attributes or {}

    def get_created_at(self):
        return self._session_attributes.get("created_at") or ""

    def get_mfa_authenticated(self):
        return self._session_attributes.get("mfa_authenticated") or ""

    def to_json(self):
        return self._session_attributes


class CTSUserInfo:
    """Represents the user that triggered a CTS event."""

    def __init__(self, user):
        self._user = user or {}

    def get_type(self):
        return self._user.get("type") or ""

    def get_principal_id(self):
        return self._user.get("principal_id") or ""

    def get_principal_urn(self):
        return self._user.get("principal_urn") or ""

    def get_account_id(self):
        return self._user.get("account_id") or ""

    def get_access_key_id(self):
        return self._user.get("access_key_id") or ""

    def get_id(self):
        return self._user.get("id") or ""

    def get_name(self):
        return self._user.get("name") or ""

    def get_domain(self):
        return CTSBaseUserDomain(self._user.get("domain"))

    def get_user_name(self):
        return self._user.get("user_name") or ""

    def get_principal_is_root_user(self):
        return self._user.get("principal_is_root_user") or ""

    def get_invoked_by(self):
        return self._user.get("invoked_by") or []

    def get_session_context(self):
        return CTSSessionContext(self._user.get("session_context"))

    def get_origin_user(self):
        return self._user.get("OriginUser") or ""

    def to_json(self):
        return self._user


__all__ = [
    "CTSEvent",
    "CTSBaseUserDomain",
    "CTSSessionContext",
    "CTSSessionContextAttributes",
    "CTSUserInfo",
]