"""
Sample timer event handler for FunctionGraph.
"""

from fg_timer_event import TimerEvent


def handler(event, context):
    """
    Main handler function for the timer event.
    
    Args:
        event (dict): The timer event data
        context: FunctionGraph execution context
        
    Returns:
        str: Response message
    """
    logger = context.getLogger()

    logger.info("Function Name: %s", context.getFunctionName())

    timer_event = TimerEvent(event)

    logger.info("Timer Event: %s", timer_event.get_trigger_name())

    return "ok"
