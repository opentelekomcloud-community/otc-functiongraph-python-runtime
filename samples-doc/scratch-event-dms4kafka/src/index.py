# coding: utf-8

from fg_dms4kafka_event import DMS4KafkaEvent


def handler(event, context):
  logger = context.getLogger()

  logger.info("Function Name: %s", context.getFunctionName())

  dms4kafka_event = DMS4KafkaEvent(event)
  
  logger.info("Trigger type: %s", dms4kafka_event.get_trigger_type())
  
  
  output = {
    "trigger_type": dms4kafka_event.get_trigger_type(),
  }
	
  return output
