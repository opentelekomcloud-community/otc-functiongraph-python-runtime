# coding: utf-8

from fg_dms4rocketmq_event import DMS4RocketMQEvent


def handler(event, context):
  logger = context.getLogger()

  logger.info("Function Name: %s", context.getFunctionName())

  dms4rocketmq_event = DMS4RocketMQEvent(event)
  
  logger.info("Trigger type: %s", dms4rocketmq_event.get_trigger_type())
  
  
  output = {
    "trigger_type": dms4rocketmq_event.get_trigger_type(),
  }
	
  return output
