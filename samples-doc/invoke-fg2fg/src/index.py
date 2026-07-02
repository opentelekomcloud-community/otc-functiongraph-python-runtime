import json
import os

from requests import request
from otc_api_sign_core import signer


def handler(event, context):
    # Get temporary AK/SK/token from context.
    ak = context.getSecurityAccessKey()
    sk = context.getSecuritySecretKey()
    token = context.getSecurityToken()

    # Get the URN of the function to invoke from user data.
    call_fg_urn = context.getUserData("CALL_FG_URN")
    region = (call_fg_urn.split(":")[2] if call_fg_urn else "") or "eu-de"

    fg_endpoint = f"https://functiongraph.{region}.otc.t-systems.com"

    # Project ID is provided by FunctionGraph runtime environment.
    project_id = os.environ.get("RUNTIME_PROJECT_ID", "")

    # Synchronous invocation endpoint. For async, use .../invocations-async instead.
    invoke_uri = f"{fg_endpoint}/v2/{project_id}/fgs/functions/{call_fg_urn}/invocations"

    body = {
        "key": "Hello FunctionGraph",
    }
    payload = json.dumps(body)

    headers = {
        "Content-Type": "application/json;charset=utf8",
        "Host": f"functiongraph.{region}.otc.t-systems.com",
        "X-Project-Id": project_id,
    }

    signed_request = signer.HttpRequest("POST", invoke_uri, headers, payload)

    sig = signer.Signer()
    sig.Key = ak
    sig.Secret = sk
    sig.SecurityToken = token
    sig.Sign(signed_request)

    response = request(
        "POST",
        invoke_uri,
        headers=signed_request.headers,
        data=payload.encode("utf-8"),
        timeout=30,
    )

    response_body = response.text
    print("Response:", response_body)

    if response.status_code >= 400:
        raise Exception(
            f"Backend request failed with status {response.status_code}: {response_body}"
        )

    return response_body
