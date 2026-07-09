import json

from fn_runtime_context import Context, Logger

class SampleEvent:
    def __init__(self, event):
        self._event = event or {}

    def get_key(self):
        return self._event.get("key", "")


def handler(event: SampleEvent, context: Context):
    logger = context.getLogger()
    
    logger.info("Function name: %s", context.getFunctionName())
    

    sample_event = SampleEvent(event)
    logger.info("Key value from event: %s", sample_event.get_key())

    output = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "isBase64Encoded": False,
        "body": json.dumps(event),
    }

    return output