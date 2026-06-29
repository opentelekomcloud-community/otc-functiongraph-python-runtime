##########################################################
# Create Test Event
##########################################################
resource "opentelekomcloud_fgs_event_v2" "test_event_post" {
  function_urn = opentelekomcloud_fgs_function_v2.MyFunction.urn
  name         = "TestEventPost"
  content = filebase64("../resources/apig_post_index.json")
}

resource "opentelekomcloud_fgs_event_v2" "test_event_get" {
  function_urn = opentelekomcloud_fgs_function_v2.MyFunction.urn
  name         = "TestEventGet"
  content = filebase64("../resources/apig_get_index.json")
}