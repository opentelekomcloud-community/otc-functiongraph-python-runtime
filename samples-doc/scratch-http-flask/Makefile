# Terraform backend configuration
BACKEND_CONFIG_BUCKET := "doc-samples-tf-backend"
BACKEND_CONFIG_KEY := "terraform_state/python/scratch-http-flask.tf"
BACKEND_CONFIG_REGION := "eu-de"
BACKEND_CONFIG_ENDPOINTS := "endpoints={s3=\"https://obs.eu-de.otc.t-systems.com\"}"

CURRENT_MAKEFILE := $(firstword $(MAKEFILE_LIST))

create_package:
	python3 ../../utils/createZip.py

tf_init:
	terraform -chdir=terraform \
	  init \
	  -backend-config=$(BACKEND_CONFIG_ENDPOINTS) \
	  -backend-config="bucket=$(BACKEND_CONFIG_BUCKET)" \
	  -backend-config="key=$(BACKEND_CONFIG_KEY)" \
	  -backend-config="region=$(BACKEND_CONFIG_REGION)"

tf_plan: 
	if [ ! -f "terraform/.terraform.lock.hcl" ]; then \
		$(MAKE) -f $(CURRENT_MAKEFILE) tf_init; \
	fi
	terraform -chdir=terraform \
	  plan \
		-var-file="variables.tfvars" 

tf_apply: create_package
	if [ ! -f "terraform/.terraform.lock.hcl" ]; then \
		$(MAKE) -f $(CURRENT_MAKEFILE) tf_init; \
	fi
	terraform -chdir=terraform \
	  apply -auto-approve \
	  -var-file="variables.tfvars"

tf_destroy:
	terraform -chdir=terraform \
	  destroy -auto-approve \
		-var-file="variables.tfvars"

test_deployed_post:
  # getting Token for authentication from Username/Password...
	$(eval OTC_X_AUTH_TOKEN := $(shell ../../utils/tokenFromUsername.sh))
	# getting the Function URN from terraform output...
	$(eval MY_FUNCTION_URN := $(shell terraform -chdir=terraform output -raw MY_FUNCTION_URN))
	# calling the deployed function via FunctionGraph API...
	@curl -X POST \
	 -H "Content-Type: application/json" \
	 -H "x-auth-token: $(OTC_X_AUTH_TOKEN)" \
	 -d @./resources/apig_post_index.json \
	 https://functiongraph.$(OTC_SDK_REGION).otc.t-systems.com/v2/$(OTC_SDK_PROJECTID)/fgs/functions/$(MY_FUNCTION_URN):latest/invocations
	@echo "" 
	# finished

test_deployed_get:
  # getting Token for authentication from Username/Password...
	$(eval OTC_X_AUTH_TOKEN := $(shell ../../utils/tokenFromUsername.sh))
	# getting the Function URN from terraform output...
	$(eval MY_FUNCTION_URN := $(shell terraform -chdir=terraform output -raw MY_FUNCTION_URN))
	# calling the deployed function via FunctionGraph API...
	@curl -X POST \
	 -H "Content-Type: application/json" \
	 -H "x-auth-token: $(OTC_X_AUTH_TOKEN)" \
	 -d @./resources/apig_get_index.json \
	 https://functiongraph.$(OTC_SDK_REGION).otc.t-systems.com/v2/$(OTC_SDK_PROJECTID)/fgs/functions/$(MY_FUNCTION_URN):latest/invocations
	@echo "" 
	# finished


test_deployed_apig_post:
	# get the API Gateway URL from terraform output
	$(eval API_GATEWAY_TRIGGER_URL := $(shell terraform -chdir=terraform output -raw API_GATEWAY_TRIGGER_URL))
	@echo "Using API Gateway URL: $(API_GATEWAY_TRIGGER_URL)"
	# execute a curl request against the deployed function via API Gateway
	curl -X POST \
	  -H 'Content-Type: application/json' \
		-d @./resources/apig_post_index.json \
		$(API_GATEWAY_TRIGGER_URL)/index
		
test_deployed_apig_get:
	# get the API Gateway URL from terraform output
	$(eval API_GATEWAY_TRIGGER_URL := $(shell terraform -chdir=terraform output -raw API_GATEWAY_TRIGGER_URL))
	@echo "Using API Gateway URL: $(API_GATEWAY_TRIGGER_URL)"
	# execute a curl request against the deployed function via API Gateway
	curl -X GET \
	   -H 'Content-Type: application/json' \
		 $(API_GATEWAY_TRIGGER_URL)/index



.PHONY: create_package tf_init tf_plan tf_apply tf_destroy test_deployed
