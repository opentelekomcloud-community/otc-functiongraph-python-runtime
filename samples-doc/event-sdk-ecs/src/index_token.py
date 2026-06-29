import os
from requests import request
import json

from fg_timer_event import TimerEvent


def handler(event, context):
    log = context.getLogger()

    timer_event = TimerEvent(event)
    timer_name = timer_event.get_trigger_name()
    user_event = timer_event.get_user_event()

    # get ecs endpoint from environment variable or use default
    ecs_endpoint = os.environ.get("ECS_ENDPOINT", "ecs.eu-de.otc.t-systems.com")

    # get project_id and instance_id from environment variables
    project_id = os.environ.get("RUNTIME_PROJECT_ID")

    # get instance_id from user data
    instance_id = context.getUserData("INSTANCE_ID")

    log.info(
        "Timer %s received with user event: %s for ECS instance: %s",
        timer_name,
        user_event,
        instance_id,
    )

    method = "POST"

    invoke_uri = f"https://{ecs_endpoint}/v1/{project_id}/cloudservers/action"

    if user_event == "start":
        body = {
            "os-start": {
                "servers": [{"id": instance_id}],
            }
        }
    elif user_event == "stop":
        body = {
            "os-stop": {
                "type": "SOFT",
                "servers": [{"id": instance_id}],
            }
        }
    else:
        log.error("Unknown user event: %s", user_event)
        return {
            "statusCode": 400,
            "isBase64Encoded": False,
            "body": json.dumps({"error": f"Unknown user event: {user_event}"}),
            "headers": {"Content-Type": "application/json"},
        }

    payload = json.dumps(body)

    token = context.getToken()

    headers = {"Content-Type": "application/json;charset=utf8", "x-auth-token": token}

    # send request
    resp = request(method, invoke_uri, headers=headers, data=payload.encode())

    return {
        "statusCode": resp.status_code,
        "isBase64Encoded": False,
        "body": resp.text,
        "headers": {"Content-Type": "application/json"},
    }
