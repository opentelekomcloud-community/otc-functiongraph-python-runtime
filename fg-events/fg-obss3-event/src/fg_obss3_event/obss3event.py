"""OBS S3 event classes for FunctionGraph."""


class OBSS3Event:
    """Represents an Object Storage Service S3 event for FunctionGraph."""

    def __init__(self, event):
        self._event = event or {}
        self._records = [OBSS3Record(record) for record in self._event.get("Records") or []]

    def get_records(self):
        return self._records

    def to_json(self):
        return self._event


class OBSS3Record:
    """Represents a single OBS S3 event record."""

    def __init__(self, record):
        self._record = record or {}

    def get_event_version(self):
        return self._record.get("eventVersion") or ""

    def get_event_time(self):
        return self._record.get("eventTime") or ""

    def get_request_parameters(self):
        return RequestParameters(self._record.get("requestParameters"))

    def get_s3(self):
        return S3Details(self._record.get("s3"))

    def get_aws_region(self):
        return self._record.get("awsRegion") or ""

    def get_event_name(self):
        return self._record.get("eventName") or ""

    def get_user_identity(self):
        return UserIdentity(self._record.get("userIdentity"))

    def to_json(self):
        return self._record


class RequestParameters:
    """Represents the request parameters in an OBS S3 event record."""

    def __init__(self, params):
        self._params = params or {}

    def get_source_ip_address(self):
        return self._params.get("sourceIPAddress") or ""

    def to_json(self):
        return self._params


class S3Details:
    """Represents the S3 payload in an OBS S3 event record."""

    def __init__(self, s3):
        self._s3 = s3 or {}

    def get_configuration_id(self):
        return self._s3.get("configurationId") or ""

    def get_object(self):
        return S3Object(self._s3.get("object"))

    def get_bucket(self):
        return S3Bucket(self._s3.get("bucket"))

    def to_json(self):
        return self._s3


class S3Object:
    """Represents the object details in an OBS S3 event."""

    def __init__(self, obj):
        self._obj = obj or {}

    def get_e_tag(self):
        return self._obj.get("eTag") or ""

    def get_sequencer(self):
        return self._obj.get("sequencer") or ""

    def get_key(self):
        return self._obj.get("key") or ""

    def get_size(self):
        return self._obj.get("size") or 0

    def to_json(self):
        return self._obj


class S3Bucket:
    """Represents the bucket details in an OBS S3 event."""

    def __init__(self, bucket):
        self._bucket = bucket or {}

    def get_arn(self):
        return self._bucket.get("arn") or ""

    def get_name(self):
        return self._bucket.get("name") or ""

    def get_owner_identity(self):
        return OwnerIdentity(self._bucket.get("ownerIdentity"))

    def to_json(self):
        return self._bucket


class OwnerIdentity:
    """Represents the bucket owner identity in an OBS S3 event."""

    def __init__(self, identity):
        self._identity = identity or {}

    def get_principal_id(self):
        return self._identity.get("PrincipalId") or ""

    def to_json(self):
        return self._identity


class UserIdentity:
    """Represents the user identity in an OBS S3 event."""

    def __init__(self, identity):
        self._identity = identity or {}

    def get_principal_id(self):
        return self._identity.get("principalId") or ""

    def to_json(self):
        return self._identity


__all__ = [
    "OBSS3Event",
    "OBSS3Record",
    "RequestParameters",
    "S3Details",
    "S3Object",
    "S3Bucket",
    "OwnerIdentity",
    "UserIdentity",
]