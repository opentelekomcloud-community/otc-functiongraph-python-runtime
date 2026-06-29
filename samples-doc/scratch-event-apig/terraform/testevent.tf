##########################################################
# Create Test Events
##########################################################

resource "opentelekomcloud_fgs_event_v2" "test_event_html" {
  function_urn = opentelekomcloud_fgs_function_v2.MyFunction.urn
  name         = "html"
  content = filebase64("../resources/apig_event_html.json")
}

resource "opentelekomcloud_fgs_event_v2" "test_event_json_b64" {
  function_urn = opentelekomcloud_fgs_function_v2.MyFunction.urn
  name         = "json_b64"
  content = filebase64("../resources/apig_event_json_b64.json")
}

resource "opentelekomcloud_fgs_event_v2" "test_event_json" {
  function_urn = opentelekomcloud_fgs_function_v2.MyFunction.urn
  name         = "json"
  content = filebase64("../resources/apig_event_json.json")
}

resource "opentelekomcloud_fgs_event_v2" "test_event_simple" {
  function_urn = opentelekomcloud_fgs_function_v2.MyFunction.urn
  name         = "simple"
  content = filebase64("../resources/apig_event.json")
}