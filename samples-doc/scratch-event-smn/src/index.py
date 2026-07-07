# coding: utf-8

from fg_smn_event import SMNEvent


def handler(event, context):
  
    logger = context.getLogger()

    logger.info("Function Name: %s", context.getFunctionName())

    smn_event = SMNEvent(event)

    logger.info("SMN Function name: %s", smn_event.get_function_name())
    logger.info("SubscriptionURN: %s", smn_event.get_records()[0].get_event_subscription_urn())

    output = {
      "function_name": smn_event.get_function_name(),
      "subscription_urn": smn_event.get_records()[0].get_event_subscription_urn(),
    }
	
    return output
