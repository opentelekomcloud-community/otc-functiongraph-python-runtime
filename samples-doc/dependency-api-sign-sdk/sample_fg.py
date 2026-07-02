# -*- coding:utf-8 -*-
import json
from requests import request
from otc_api_sign_core import signer

def handler (event, context):

    ecs_endpoint ="ecs.eu-de.otc.t-systems.com"
    project_id="d52e41d2434941b194ce3f91b1b12f8a"
    method = "POST"

    invoke_uri = f"https://{ecs_endpoint}/v1/{project_id}/cloudservers/action"

    body = {
            "os-start": {
                "servers": [{"id": "cdb29bdd-1235-4e98-90d3-34bb77450393"}],
            }
        }
    headers = {
        "Content-Type": "application/json;charset=utf8",
        "Host": ecs_endpoint,
        "X-Project-Id": project_id,
    }

    payload = json.dumps(body)

    sig = signer.Signer()
    sig.Key = context.getSecurityAccessKey()
    sig.Secret = context.getSecuritySecretKey()
    sig.SecurityToken = context.getSecurityToken()

    signed_request = signer.HttpRequest(method, invoke_uri, headers, payload)

    sig.Sign(signed_request)

    resp = request(
        method, invoke_uri, headers=signed_request.headers, data=payload.encode()
    )

    return {
        "statusCode": resp.status_code,
        "isBase64Encoded": False,
        "body": resp.text,
        "headers": {"Content-Type": "application/json"},
    }