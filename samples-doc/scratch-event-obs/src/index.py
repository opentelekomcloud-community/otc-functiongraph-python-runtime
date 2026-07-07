# coding: utf-8

"""
Sample obs event handler for FunctionGraph.
"""

from fg_obss3_event import OBSS3Event


def handler(event, context):
    """
    Main handler function for the OBS event.
    
    Args:
        event (dict): The OBS event data
        context: FunctionGraph execution context
        
    Returns:
        str: Response message
    """
    logger = context.getLogger()

    logger.info("Function Name: %s", context.getFunctionName())

    obs_event = OBSS3Event(event)

    logger.info("OBS Event: %s", obs_event.get_records()[0].get_event_name())
    logger.info("OBS Event - Bucket: %s", obs_event.get_records()[0].get_s3().get_bucket().get_name())

    output = {
      "event_name": obs_event.get_records()[0].get_event_name(),
      "bucketname": obs_event.get_records()[0].get_s3().get_bucket().get_name(),
    }
	
    return output
