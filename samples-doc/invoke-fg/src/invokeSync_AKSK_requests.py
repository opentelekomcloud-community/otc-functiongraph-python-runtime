import json
import os
import sys

from otc_api_sign_core import signer

try:
    from requests import request
except ImportError:
    request = None


def main() -> int:
    if request is None:
        print(
            "Missing dependency: requests. Install it with 'pip install requests'.",
            file=sys.stderr,
        )
        return 1

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

    invoke_uri = f"{fg_endpoint}/v2/{project_id}/fgs/functions/{function_urn}/invocations"
    print("Invoke URI:", invoke_uri)

    x_cff_log_type = "tail"
    x_cff_request_version = "v1"

    body = {
        "key": "Hello T-Cloud Public World - SYNC",
    }
    payload = json.dumps(body)

    method = "POST"
    headers = {
        "Content-Type": "application/json;charset=utf8",
        "Host": f"functiongraph.{region}.otc.t-systems.com",
        "X-Cff-Log-Type": x_cff_log_type,
        "X-CFF-Request-Version": x_cff_request_version,
        "X-Project-Id": project_id,
    }

    sig = signer.Signer()
    sig.Key = ak
    sig.Secret = sk

    signed_request = signer.HttpRequest(method, invoke_uri, headers, payload)
    sig.Sign(signed_request)

    try:
        response = request(
            method,
            invoke_uri,
            headers=signed_request.headers,
            data=payload.encode("utf-8"),
            timeout=30,
        )
        data = response.json()
        print("Status:", response.status_code)
        print("Result:", data.get("result"))
        print("Log:", data.get("log"))
    except Exception as exc:
        print("Error:", exc, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
