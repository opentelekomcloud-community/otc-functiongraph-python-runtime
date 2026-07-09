import threading
import logging
import time
import copy


# MAX_ROW_SIZE max row size of a log
MAX_ROW_SIZE = 1024
# python logging config
LOG_FORMAT = "[%(asctime)s %(levelname)s %(filename)s:%(lineno)d]" \
             " [%(podname)s %(thread)d] %(message)s"
# MAX_SINGLE_LOG_SIZE max single log size 90KB
MAX_SINGLE_LOG_SIZE = 90 * 1024


def get_time_offset():
    """Method get_time_offset"""
    is_dst = time.daylight and time.localtime().tm_isdst > 0
    return -(time.altzone if is_dst else time.timezone)


def get_formated_time_offset():
    """Method get_formated_time_offset"""
    result = "+"
    offset = get_time_offset()
    if offset < 0:
        result = "-"
        offset = -offset

    result += "%02d:%02d" % (int(offset / 3600), offset % 60)
    return result


class FunctionLoggerImpl(logging.StreamHandler):
    """Class LoggerImpl"""

    log_writer = None

    def __init__(self, invoke_id, trace_id):
        self.invoke_id = invoke_id
        self.trace_id = trace_id
        global _INVOKE_ID
        _INVOKE_ID = invoke_id
        global _TRACE_ID
        _TRACE_ID = trace_id
        super().__init__()

    def emit(self, record):
        """Method emit"""
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%dT%H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000000000
        time_stamp = "%s.%09d" % (data_head, data_secs) + get_formated_time_offset()

        lines = split_message(record.getMessage())
        trace_id = self.trace_id or ""
        invoke_id = self.invoke_id or ""
        for line in lines:
            rec = copy.copy(record)
            rec.args = None
            rec.msg = "%s %s %s %s %s" % (
                time_stamp,
                trace_id,
                invoke_id,
                record.levelname,
                line,
            )
            super().emit(rec)


def acquire_function_logger(invoke_id, request_id):
    """Method acquire_logger"""
    current_thread = threading.current_thread()
    function_logger = logging.getLogger(str(current_thread.ident))
    function_logger = logging.getLogger()
    function_logger.setLevel(logging.INFO)

    function_logger.propagate = 0
    logger_handler = FunctionLoggerImpl(invoke_id, request_id)
    function_logger.addHandler(logger_handler)

    return function_logger


def split_message(message):
    """Method split message to list of lines"""
    lines = []
    if isinstance(message, bytes):
        message = message.decode("utf-8")
    split_count = len(message) // MAX_SINGLE_LOG_SIZE
    remainder = len(message) % MAX_SINGLE_LOG_SIZE
    if remainder == 0:
        if split_count == 0:
            lines.append(message)
        for i in range(split_count):
            lines.append(
                message[MAX_SINGLE_LOG_SIZE * i : MAX_SINGLE_LOG_SIZE * (i + 1)]
            )
    else:
        for i in range(split_count + 1):
            if i < split_count:
                lines.append(
                    message[MAX_SINGLE_LOG_SIZE * i : MAX_SINGLE_LOG_SIZE * (i + 1)]
                )
            else:
                lines.append(message[MAX_SINGLE_LOG_SIZE * i :])
    return lines
