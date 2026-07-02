"use strict";
const https = require("https");

exports.handler = async function (event, context) {

  const logger = context.getLogger();
  const token = context.getToken();

  
  // get the URN of the function to be called from user data
  const CALL_FG_URN = context.getUserData("CALL_FG_URN");

  // get region from function URN
  const region = CALL_FG_URN.split(":")[2] || "eu-de";

  // FunctionGraph endpoint
  const fgEndpoint = `https://functiongraph.${region}.otc.t-systems.com`;

  // get projectId from Runtime environment variable (set in FG backend)
  const projectId = context.getProjectID();

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
    "x-auth-token": token,
  };

  
  return new Promise((resolve, reject) => {
    const req = https.request(invokeURI, { method: "POST", headers }, (res) => {
      res.setEncoding("utf8");

      let responseBody = "";
      res.on("data", (chunk) => {
        responseBody += chunk;
      });

      res.on("end", () => {
        logger.info("Response: ", responseBody);
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
