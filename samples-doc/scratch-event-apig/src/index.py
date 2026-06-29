import json

from fg_apig_event import APIGEvent, APIGResponse


def handler(event, context):
	logger = context.getLogger()

	logger.info("Function Name: %s", context.getFunctionName())

	apig_event = APIGEvent(event)
	is_base64_encoded = apig_event.is_base64_encoded() or False

	body = apig_event.get_body()
	logger.info("APIG Event body: %s", body)

	response_type = apig_event.get_query_string_parameter("responseType")

	if response_type == "html":
		output = APIGResponse(
			200,
			"",
			{"Content-Type": "text/html; charset=utf-8"},
			False,
		)
		output.set_body(
			"<html><h1>Welcome to use FunctionGraph</h1></html>",
			is_base64_encoded,
		)
	elif response_type == "json":
		output = APIGResponse(
			200,
			"",
			{"Content-Type": "application/json"},
			False,
		)
		try:
			parsed_body = json.loads((body or "").replace('\\"', '"'))
			output.set_body(parsed_body, is_base64_encoded)
		except (json.JSONDecodeError, TypeError):
			output.set_body({"error": "Invalid JSON input"}, is_base64_encoded)
	else:
		output = APIGResponse(
			200,
			"",
			{"Content-Type": "text/html; charset=utf-8"},
			False,
		)
		output.set_body(
			"<html>Please construct the url with query parameters responseType=html, responseType=json</html>",
			is_base64_encoded,
		)

	logger.info("returning: %s", output)

	return output
