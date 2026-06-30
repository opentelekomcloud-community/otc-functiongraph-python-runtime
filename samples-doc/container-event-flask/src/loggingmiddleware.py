from datetime import datetime, timezone

from flask import g, request


class RequestLogger:
    def __init__(self, request_id: str):
        self.request_id = request_id

    @staticmethod
    def _timestamp() -> str:
        # Match JS toISOString style with millisecond precision and UTC marker.
        return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

    def log(self, *args) -> None:
        print(f"{self._timestamp()} [{self.request_id}]", *args, flush=True)
        
    def debug(self, *args) -> None:
        print(f"{self._timestamp()} [DEBUG] [{self.request_id}]", *args, flush=True)

    def info(self, *args) -> None:
        print(f"{self._timestamp()} [INFO] [{self.request_id}]", *args, flush=True)

    def warn(self, *args) -> None:
        print(f"{self._timestamp()} [WARN] [{self.request_id}]", *args, flush=True)

    def error(self, *args) -> None:
        print(f"{self._timestamp()} [ERROR] [{self.request_id}]", *args, flush=True)


def register_logging_middleware(app):
    @app.before_request
    def _before_request() -> None:
        incoming_request_id = request.headers.get("X-Cff-Request-Id")
        request_id = incoming_request_id or "no-request-id"

        # Keep request-scoped values aligned with original middleware behavior.
        g.cff_request_id = request_id
        g.logger = RequestLogger(request_id)

    @app.after_request
    def _after_request(response):
        incoming_request_id = request.headers.get("X-Cff-Request-Id")
        if incoming_request_id:
            response.headers["x-cff-request-id"] = incoming_request_id
        return response
