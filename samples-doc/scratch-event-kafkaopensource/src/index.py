# coding: utf-8

from fg_kafkaopensource_event import KafkaOpenSourceEvent


def handler(event, context):
  logger = context.getLogger()

  logger.info("Function Name: %s", context.getFunctionName())

  kafka_opensource_event = KafkaOpenSourceEvent(event)
  
  logger.info("Trigger type: %s", kafka_opensource_event.get_trigger_type())
  
  
  output = {
    "trigger_type": kafka_opensource_event.get_trigger_type(),
  }
	
  return output
