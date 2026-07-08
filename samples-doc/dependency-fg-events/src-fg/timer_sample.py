# -*- coding:utf-8 -*-
from fg_timer_event import TimerEvent
 
def handler(event, context):

    logger = context.getLogger()

    logger.info("Function  Name: %s", context.getFunctionName())

    timer_event = TimerEvent(event)

    logger.info("Timer Event: %s", timer_event.get_trigger_name())
    
    output = {        
        "trigger_name": timer_event.get_trigger_name(),
        "trigger_time": timer_event.get_time(),
        "trigger_type": timer_event.get_trigger_type()
    }

    return output
