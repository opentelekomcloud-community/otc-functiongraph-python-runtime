"""
TimerEvent class for FunctionGraph timer events.
"""

import json


class TimerEvent:
    """
    Represents a Timer event for FunctionGraph.

    Attributes:
        version (str): Event version
        time (str): Event time
        trigger_type (str): Trigger type
        trigger_name (str): Trigger name
        user_event (str): User event data
    """

    def __init__(self, event):
        """
        Initialize TimerEvent.

        Args:
            event (dict): The timer event data
        """
        self._event = event or {}

    def get_version(self):
        """
        Returns the event version.

        Returns:
            str: Event version
        """
        return self._event.get("version") or ""

    def get_time(self):
        """
        Returns the event time.

        Returns:
            str: Event time
        """
        return self._event.get("time") or ""

    def get_trigger_type(self):
        """
        Returns the trigger type.

        Returns:
            str: Trigger type
        """
        return self._event.get("trigger_type") or ""

    def get_trigger_name(self):
        """
        Returns the trigger name.

        Returns:
            str: Trigger name
        """
        return self._event.get("trigger_name") or ""

    def get_user_event(self):
        """
        Returns the user event.

        Returns:
            str: User event
        """
        return self._event.get("user_event") or ""

    def get_user_event_parsed(self):
        """
        Returns the parsed user event, or None if parsing fails.

        Returns:
            dict or None: The parsed user event data, or None if invalid JSON
        """
        try:
            result = json.loads(self._event.get("user_event"))
            return result
        except (json.JSONDecodeError, TypeError):
            return None

    def to_json(self):
        """
        Returns the event as a dictionary.

        Returns:
            dict: The raw event data
        """
        return self._event


# Export class for use in other modules
__all__ = ["TimerEvent"]