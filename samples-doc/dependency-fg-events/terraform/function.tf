##########################################################
# Create Python event function
##########################################################
resource "opentelekomcloud_fgs_function_v2" "MyFunction" {

  name = "py310_fg-events-dependency-sample"
  app  = "default"

  handler = "timer_sample.handler"

  runtime = "Python3.10"

  code_type     = "inline"
  func_code     = filebase64(format("${path.module}/../%s", "src-fg/timer_sample.py"))
  code_filename = "timer_sample.py"

  description      = "sample on how to use dependency package fg-events"
  memory_size      = 128
  timeout          = 30
  max_instance_num = 1

  depend_list = [
    opentelekomcloud_fgs_dependency_version_v2.dep_3_10.version_id
  ]

  lifecycle  {
    create_before_destroy=true
 }

}

output "MY_FUNCTION_URN" {
  value = opentelekomcloud_fgs_function_v2.MyFunction.urn
}

output "MY_FUNCTION_VERSION" {
  value = opentelekomcloud_fgs_function_v2.MyFunction.version
}

##########################################################
# Create Test Event
##########################################################
resource "opentelekomcloud_fgs_event_v2" "test_event_post" {
  function_urn = opentelekomcloud_fgs_function_v2.MyFunction.urn
  name         = "TestEventPost"
  content = base64encode(jsonencode({
    "version"      = "v1.0",
    "time"         = "2026-06-01T08:30:00+08:00",
    "trigger_type" = "TIMER",
    "trigger_name" = "Timer_001",
    "user_event"   = "{\"message\": \"timer triggered event\", \"topic\":\"test\"}"
  }))
}
