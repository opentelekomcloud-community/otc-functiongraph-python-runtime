import json
import os
import sys
from urllib import request as urllib_request

from otc_api_sign_core import signer


def main() -> int:
    region = os.getenv("OTC_SDK_REGION", "eu-de")
    project_id = os.getenv("OTC_SDK_PROJECTID")
    ak = os.getenv("OTC_SDK_AK")
    sk = os.getenv("OTC_SDK_SK")

    missing = [
        name
        for name, value in [
            ("OTC_SDK_PROJECTID", project_id),
            ("OTC_SDK_AK", ak),
            ("OTC_SDK_SK", sk),
        ]
        if not value
    ]
    if missing:
        print(f"Missing required environment variables: {', '.join(missing)}", file=sys.stderr)
        return 1

    fg_endpoint = f"https://functiongraph.{region}.otc.t-systems.com"
    function_name = "python-sample-invoke-function"
    function_version = "latest"
    function_app = "default"

    function_urn = (
        f"urn:fss:{region}:{project_id}:function:{function_app}:{function_name}:{function_version}"
    )

    invoke_uri = (
        f"{fg_endpoint}/v2/{project_id}/fgs/functions/{function_urn}/invocations-async"
    )
    print("Invoke URI:", invoke_uri)

    body = {
        "key": "Hello T-Cloud Public World - ASYNC ",
    }
    payload = json.dumps(body)

    method = "POST"
    headers = {
        "Content-Type": "application/json;charset=utf8",
        "Host": f"functiongraph.{region}.otc.t-systems.com",
        "X-Project-Id": project_id,
    }

    sig = signer.Signer()
    sig.Key = ak
    sig.Secret = sk

    signed_request = signer.HttpRequest(method, invoke_uri, headers, payload)
    sig.Sign(signed_request)

    http_request = urllib_request.Request(
        invoke_uri,
        data=payload.encode("utf-8"),
        headers=signed_request.headers,
        method=method,
    )

    try:
        with urllib_request.urlopen(http_request) as response:
            response_body = response.read().decode("utf-8")
            print("Status:", response.status)
            print("Response:", response_body)
    except Exception as exc:
        print("Error:", exc, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
