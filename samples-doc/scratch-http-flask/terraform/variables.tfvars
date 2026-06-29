# prefix of all resources
prefix        = "python"

# description of the function
description = "Sample scratch-http-flask"

# name of the function (will be prefixed)
function_name = "scratch-http-flask"

# name of zip file to deploy
zip_file_name = "dist/code.zip"

# resources will be tagged with this app_group tag
tag_app_group = "scratch-http-flask"

# change to your API Gateway instance ID
# set as env var TF_VAR_API_GATEWAY_INSTANCE_ID or uncomment and set here
#API_GATEWAY_INSTANCE_ID="YOUR_API_GATEWAY_INSTANCE_ID"
