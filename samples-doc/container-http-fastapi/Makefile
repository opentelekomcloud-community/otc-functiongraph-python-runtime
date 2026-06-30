SHELL:=/bin/bash
TARGET_PATH=target

CURRENT_MAKEFILE := $(firstword $(MAKEFILE_LIST))

# Docker build configuration
DOCKER_FILE=Dockerfile
IMAGE_NAME=custom_container_http_fastapi_python

# Terraform backend configuration
BACKEND_CONFIG_BUCKET := "doc-samples-tf-backend"
BACKEND_CONFIG_KEY := "terraform_state/python/python-container-http-fastapi.tf"
BACKEND_CONFIG_REGION := "eu-de"
BACKEND_CONFIG_ENDPOINTS := "endpoints={s3=\"https://obs.eu-de.otc.t-systems.com\"}"


#############################################################################################
# Docker targets
#############################################################################################

build: clean

docker_build: 
	docker buildx build \
	  --platform linux/amd64 \
		--file $(DOCKER_FILE) \
		--tag $(IMAGE_NAME):latest .

docker_run_local:
	docker container run \
	  --rm \
		--platform linux/amd64 \
		--publish 8000:8000 \
		--user 1003:1003 \
		--name $(IMAGE_NAME) \
		$(IMAGE_NAME):latest

docker_push: docker_build
  # see: https://docs.otc.t-systems.com/software-repository-container/umn/image_management/obtaining_a_long-term_valid_login_command.html#swr-01-1000
	docker login -u $(OTC_SDK_PROJECTNAME)@$(OTC_SDK_AK) -p $(OTC_SWR_LOGIN_KEY) $(OTC_SWR_ENDPOINT)
	docker tag $(IMAGE_NAME):latest $(OTC_SWR_ENDPOINT)/$(OTC_SWR_ORGANIZATION)/$(IMAGE_NAME):latest
	docker push $(OTC_SWR_ENDPOINT)/$(OTC_SWR_ORGANIZATION)/$(IMAGE_NAME):latest

docker_all: build docker_push

clean:
	rm -rf $(TARGET_PATH)

all: build docker_build

#############################################################################################
# Terraform targets
#############################################################################################
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
		-var-file="variables.tfvars" \
		-var="image_url=$(OTC_SWR_ENDPOINT)/$(OTC_SWR_ORGANIZATION)/$(IMAGE_NAME):latest"

tf_apply: docker_push
	if [ ! -f "terraform/.terraform.lock.hcl" ]; then \
		$(MAKE) -f $(CURRENT_MAKEFILE) tf_init; \
	fi
	terraform -chdir=terraform \
	  apply -auto-approve \
	  -var-file="variables.tfvars" \
		-var="image_url=$(OTC_SWR_ENDPOINT)/$(OTC_SWR_ORGANIZATION)/$(IMAGE_NAME):latest"

tf_destroy:
	terraform -chdir=terraform \
	  destroy -auto-approve \
		-var-file="variables.tfvars" \
		-var="image_url=$(OTC_SWR_ENDPOINT)/$(OTC_SWR_ORGANIZATION)/$(IMAGE_NAME):latest"

#############################################################################################
# Test targets
#############################################################################################
test_local:
  # execute a curl 
	curl -X POST \
	-H "X-Cff-Request-Id: $(shell uuidgen)" \
	-H "X-Cff-Func-Name: 0@default@sample-container-http-fastapi" \
	-H "X-Cff-Func-Version: latest" \
	-H "X-Cff-Func-Timeout: 30" \
	-H 'Content-Type: application/json' \
	-d '{"key":"Hello World of FunctionGraph"}' localhost:8000/invoke
	@echo ""

test_deployed:
  # getting Token for authentication from Username/Password...
	$(eval OTC_X_AUTH_TOKEN := $(shell ../../utils/tokenFromUsername.sh))
	# getting the Function URN from terraform output...
	$(eval MY_FUNCTION_URN := $(shell terraform -chdir=terraform output -raw MY_FUNCTION_URN))
	# calling the deployed function via FunctionGraph API...
	@curl -X POST \
	 -H "Content-Type: application/json" \
	 -H "x-auth-token: $(OTC_X_AUTH_TOKEN)" \
	 -d '{"key":"Hello World of FunctionGraph"}' \
	 https://functiongraph.$(OTC_SDK_REGION).otc.t-systems.com/v2/$(OTC_SDK_PROJECTID)/fgs/functions/$(MY_FUNCTION_URN):latest/invocations
	@echo "" 
	# finished

.PHONY: build run_local docker_build docker_run_local docker_push docker_all test_local test_deployed clean tf_init tf_plan tf_apply tf_destroy
