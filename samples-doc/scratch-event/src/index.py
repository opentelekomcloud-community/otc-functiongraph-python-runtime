import json

class SampleEvent:
    def __init__(self, event):
        self._event = event or {}

    def get_key(self):
        return self._event.get("key", "")


def initializer(context):
    logger = context.getLogger()
    logger.info("initializing : %s", context.getFunctionName())


def handler(event, context):
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