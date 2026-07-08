resource "opentelekomcloud_fgs_dependency_version_v2" "dep_3_6" {
  name    = "fg-events-${var.dependency_version}-python-3.6"
  runtime = "Python3.6"
  file    = filebase64("${path.module}/../dist/code.zip")
  description = "fg-events (https://github.com/opentelekomcloud-community/otc-functiongraph-python-runtime/tree/main/samples-doc/dependency-fg-events)"
}

resource "opentelekomcloud_fgs_dependency_version_v2" "dep_3_9" {
  name    = "fg-events-${var.dependency_version}-python-3.9"
  runtime = "Python3.9"
  file    = filebase64("${path.module}/../dist/code.zip")
  description = "fg-events (https://github.com/opentelekomcloud-community/otc-functiongraph-python-runtime/tree/main/samples-doc/dependency-fg-events)"
}

resource "opentelekomcloud_fgs_dependency_version_v2" "dep_3_10" {
  name    = "fg-events-${var.dependency_version}-python-3.10"
  runtime = "Python3.10"
  file    = filebase64("${path.module}/../dist/code.zip")
  description = "fg-events (https://github.com/opentelekomcloud-community/otc-functiongraph-python-runtime/tree/main/samples-doc/dependency-fg-events)"
}

resource "opentelekomcloud_fgs_dependency_version_v2" "dep_3_12" {
  name    = "fg-events-${var.dependency_version}-python-3.12"
  runtime = "Python3.12"
  file    = filebase64("${path.module}/../dist/code.zip")
  description = "fg-events (https://github.com/opentelekomcloud-community/otc-functiongraph-python-runtime/tree/main/samples-doc/dependency-fg-events)"
}
