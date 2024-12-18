IMAGE_NAME                       ?= "noName"
IMAGE_TAG                        ?= ""
NAMESPACE                        ?= ""
MSG                              ?= "Default MSG"
FILE_PATH                        ?= .
GITHUB_SHA                       ?= ""
DOCKER_USERNAME                  = $(shell echo $$DOCKER_USERNAME)
DOCKER_PASSWORD                  = $(shell echo $$DOCKER_PASSWORD)
AWS_REGION                       = $(shell echo $$AWS_REGION)
EKS_NAME                         = $(shell echo $$EKS_NAME)


docker_login:
	echo "$(DOCKER_PASSWORD)" | docker login -u "$(DOCKER_USERNAME)" --password-stdin

docker_build:
	docker build -t "$(DOCKER_USERNAME)/${IMAGE_NAME}:${NAMESPACE}_${IMAGE_TAG}" $(FILE_PATH)
	echo docker images

docker_tag:
	docker tag "$(DOCKER_USERNAME)/${IMAGE_NAME}:${NAMESPACE}_${IMAGE_TAG}" "$(DOCKER_USERNAME)/$(IMAGE_NAME):$(NAMESPACE)_${GITHUB_SHA}"
	docker images

docker_push:
	docker push "$(DOCKER_USERNAME)/${IMAGE_NAME}:${NAMESPACE}_${IMAGE_TAG}"
	echo "Successfully pushed: $(DOCKER_USERNAME)/${IMAGE_NAME}:${NAMESPACE}_${IMAGE_TAG}"
	docker push "$(DOCKER_USERNAME)/$(IMAGE_NAME):$(NAMESPACE)_${GITHUB_SHA}"
	echo "Successfully pushed: $(DOCKER_USERNAME)/$(IMAGE_NAME):$(NAMESPACE)_${GITHUB_SHA}"

kubectl:
	curl -LO "https://dl.k8s.io/release/v1.23.3/bin/linux/amd64/kubectl"
	chmod +x ./kubectl
	sudo mv ./kubectl /usr/local/bin/kubectl

kubeconfig:
	aws eks update-kubeconfig --name $(EKS_NAME) --region $(AWS_REGION)

helm:
	curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
	sudo apt-get install apt-transport-https --yes
	echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
	sudo apt-get update -y
	sudo apt-get install helm -y

echo_debug:
	echo "----Debug_$(MSG)"
