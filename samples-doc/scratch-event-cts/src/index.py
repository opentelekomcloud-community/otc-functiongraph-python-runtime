# -*- coding:utf-8 -*-
from fg_cts_event import CTSEvent
 
def handler(event, context):
  logger = context.getLogger()

  logger.info("Function Name: %s", context.getFunctionName())

  cts_event = CTSEvent(event)
 
  logger.info("CTS Event- Trace type: %s", cts_event.get_trace_type())
  logger.info("CTS Event- Service type: %s", cts_event.get_service_type())

  output = {
    "service_type": cts_event.get_service_type(),
    "trace_type": cts_event.get_trace_type(),
    "trace_name": cts_event.get_trace_name(),
  }
	
  return output
