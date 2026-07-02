import json

from requests import request


def handler(event, context):
    logger = context.getLogger()
    token = context.getToken()

    # Get the URN of the function to invoke from user data.
    call_fg_urn = context.getUserData("CALL_FG_URN")

    # Get region from function URN.
    region = (call_fg_urn.split(":")[2] if call_fg_urn else "") or "eu-de"

    # FunctionGraph endpoint.
    fg_endpoint = f"https://functiongraph.{region}.otc.t-systems.com"

    # Get project ID from runtime context.
    project_id = context.getProjectID()

    # Synchronous invocation endpoint. For async, use .../invocations-async instead.
    invoke_uri = f"{fg_endpoint}/v2/{project_id}/fgs/functions/{call_fg_urn}/invocations"

    body = {
        "key": "Hello FunctionGraph",
    }
    payload = json.dumps(body)

    headers = {
        "Content-Type": "application/json;charset=utf8",
        "x-auth-token": token,
    }

    response = request(
        "POST",
        invoke_uri,
        headers=headers,
        data=payload.encode("utf-8"),
        timeout=30,
    )

    response_body = response.text
    logger.info("Response: %s", response_body)

    if response.status_code >= 400:
        raise Exception(
            f"Backend request failed with status {response.status_code}: {response_body}"
        )

    return response_body
