# coding: utf-8

from fg_lts_event import LTSEvent


def handler(event, context):
  logger = context.getLogger()

  logger.info("Function Name: %s", context.getFunctionName())

  lts_event = LTSEvent(event)
  
  logger.info("logs: %s", lts_event.get_logs())
  
  
  output = {
    "logs": lts_event.get_logs(),
  }
	
  return output
