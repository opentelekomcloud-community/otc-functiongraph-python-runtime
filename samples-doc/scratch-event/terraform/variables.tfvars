# Terraform variables for scratch-event-async sample

# prefix of all resources
prefix        = "python"

# description of the function
description = "Sample scratch-event"

# name of the function (will be prefixed)
function_name = "scratch-event"

# handler function name defined in your code, e.g. "index.handler"
handler_name = "index.handler"

# initializer function name defined in your code, e.g. "index.initializer"
initializer_name = "index.initializer"

# name of zip file to deploy
zip_file_name = "scratch-event.zip"

# resources will be tagged with this app_group tag
tag_app_group = "scratch-event"
