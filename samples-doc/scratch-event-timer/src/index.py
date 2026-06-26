"""
Sample timer event handler for FunctionGraph.
"""

from fg_timer_event import TimerEvent


def initializer(context, callback):
    """
    Initialization function called when the function is created.
    
    Args:
        context: FunctionGraph execution context
        callback: Callback function to signal completion
    """
    logger = context.getLogger()
    logger.info("Function initialized")
    callback(None, "")


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
