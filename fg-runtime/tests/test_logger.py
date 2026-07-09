import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fn_runtime_context.logger import Logger, MAX_SINGLE_LOG_SIZE


class LoggerTests(unittest.TestCase):
    def test_info_formats_percent_style_messages(self):
        logger = Logger("request-1", "invoke-1")

        with patch("fn_runtime_context.logger._get_time", return_value="2024-01-01T00:00:00.000Z"):
            output = io.StringIO()
            with redirect_stdout(output):
                logger.info("Function Name: %s", "demo")

        self.assertEqual(
            output.getvalue().strip(),
            "2024-01-01T00:00:00.000Z request-1 invoke-1 INFO Function Name: demo",
        )

    def test_debug_respects_log_level(self):
        logger = Logger("request-1")
        output = io.StringIO()

        with redirect_stdout(output):
            logger.debug("hidden")

        self.assertEqual(output.getvalue(), "")

        logger.setLevel("DEBUG")
        with patch("fn_runtime_context.logger._get_time", return_value="2024-01-01T00:00:00.000Z"):
            output = io.StringIO()
            with redirect_stdout(output):
                logger.debug("visible")

        self.assertEqual(
            output.getvalue().strip(),
            "2024-01-01T00:00:00.000Z request-1 DEBUG visible",
        )

    def test_warn_and_error_emit_expected_levels(self):
        logger = Logger("request-1")

        with patch("fn_runtime_context.logger._get_time", return_value="2024-01-01T00:00:00.000Z"):
            output = io.StringIO()
            with redirect_stdout(output):
                logger.warn("warning")
                logger.error("error")

        lines = output.getvalue().strip().splitlines()
        self.assertEqual(lines[0], "2024-01-01T00:00:00.000Z request-1 WARN warning")
        self.assertEqual(lines[1], "2024-01-01T00:00:00.000Z request-1 ERROR error")

    def test_long_messages_are_split(self):
        logger = Logger("request-1")
        long_message = "x" * (MAX_SINGLE_LOG_SIZE + 5)

        with patch("fn_runtime_context.logger._get_time", return_value="2024-01-01T00:00:00.000Z"):
            output = io.StringIO()
            with redirect_stdout(output):
                logger.info(long_message)

        self.assertEqual(len(output.getvalue().strip().splitlines()), 2)


if __name__ == "__main__":
    unittest.main()