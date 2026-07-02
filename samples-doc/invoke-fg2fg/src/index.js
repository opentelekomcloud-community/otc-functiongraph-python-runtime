"use strict";
const https = require("https");

const {
  Signer,
  HttpRequest,
} = require("@opentelekomcloud-community/otc-api-sign-sdk-nodejs");

exports.handler = async function (event, context) {
  // get temporary ak/sk/token from context
  // to use, an agency with permission to invoke FunctionGraph is needed:
  const ak = context.getSecurityAccessKey();
  const sk = context.getSecuritySecretKey();
  const token = context.getSecurityToken();

  // get the URN of the function to be called from user data
  const CALL_FG_URN = context.getUserData("CALL_FG_URN");

  // get region from function URN
  const region = CALL_FG_URN.split(":")[2] || "eu-de";

  // FunctionGraph endpoint
  const fgEndpoint = `https://functiongraph.${region}.otc.t-systems.com`;

  // get projectId from Runtime environment variable (set in FG backend)
  const projectId = process.env.RUNTIME_PROJECT_ID || "";

  // Endpoint for asynchronous invocation
  // const invokeURI = `${fgEndpoint}/v2/${projectId}/fgs/functions/${CALL_FG_URN}/invocations-async`;
  // or synchronous invocation
  const invokeURI = `${fgEndpoint}/v2/${projectId}/fgs/functions/${CALL_FG_URN}/invocations`;

  // set body according to your function input
  const body = {
    key: "Hello FunctionGraph",
  };
  const payload = JSON.stringify(body);

  // set headers
  const headers = {
    "Content-Type": "application/json;charset=utf8",
    Host: new URL(fgEndpoint).host,
    "X-Project-Id": projectId,
  };

  // create HttpRequest instance
  const request = new HttpRequest("POST", invokeURI, headers, payload);

  // create Signer instance and use temporary ak/sk/token to sign the request
  const signer = new Signer();
  signer.Key = ak;
  signer.Secret = sk;
  signer.SecurityToken = token;

  // sign the request
  const signedRequest = signer.Sign(request);

  // send the signed request
  return new Promise((resolve, reject) => {
    const req = https.request(signedRequest, (res) => {
      res.setEncoding("utf8");

      let responseBody = "";
      res.on("data", (chunk) => {
        responseBody += chunk;
      });

      res.on("end", () => {
        console.log("Response: ", responseBody);
        if (res.statusCode && res.statusCode >= 400) {
          reject(
            new Error(
              `Backend request failed with status ${res.statusCode}: ${responseBody}`,
            ),
          );
          return;
        }

        resolve(responseBody);
      });
    });

    req.on("error", reject);
    req.write(payload);
    req.end();
  });
};
