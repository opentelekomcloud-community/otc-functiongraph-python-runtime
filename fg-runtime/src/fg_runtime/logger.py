"""Logger implementation for the FunctionGraph Python runtime."""

from datetime import datetime, timezone


MAX_SINGLE_LOG_SIZE = 90 * 1024


def _get_time():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )


def _split_string(value):
    if not value:
        return [""]

    return [
        value[index : index + MAX_SINGLE_LOG_SIZE]
        for index in range(0, len(value), MAX_SINGLE_LOG_SIZE)
    ]


def _format_message(*args):
    if not args:
        return ""

    first_arg = args[0]
    if isinstance(first_arg, str) and len(args) > 1:
        try:
            return first_arg % args[1:]
        except (TypeError, ValueError):
            pass

    return " ".join(str(arg) for arg in args)


def _send_log(level, only_message, invoke_id, request_id, *args):
    message = _format_message(*args)
    lines = _split_string(message)
    spaced_invoke_id = f" {invoke_id} " if invoke_id else " "

    for line in lines:
        if not only_message:
            print(f"{_get_time()} {request_id}{spaced_invoke_id}{level} {line}")
        else:
            print(f"{request_id}{spaced_invoke_id}{level} {line}")


class Logger:
    """Simple stdout logger matching the FunctionGraph JS runtime surface."""

    def __init__(self, request_id, invoke_id=""):
        self.request_id = request_id
        self.invoke_id = invoke_id
        self.log_level = "INFO"

    def set_level(self, level):
        if level in {"INFO", "ERROR", "WARN", "DEBUG"}:
            self.log_level = level

    def info(self, *args):
        if self.log_level in {"INFO", "DEBUG"}:
            _send_log("INFO", False, self.invoke_id, self.request_id, *args)

    def error(self, *args):
        _send_log("ERROR", False, self.invoke_id, self.request_id, *args)

    def warn(self, *args):
        if self.log_level in {"INFO", "WARN", "DEBUG"}:
            _send_log("WARN", False, self.invoke_id, self.request_id, *args)

    def debug(self, *args):
        if self.log_level == "DEBUG":
            _send_log("DEBUG", False, self.invoke_id, self.request_id, *args)


__all__ = ["Logger", "MAX_SINGLE_LOG_SIZE"]