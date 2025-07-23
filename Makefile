.PHONY: help install db dp dev start lint test image push docker-compose-start deploy-k8s doc pypi clean

# Variables
TAG ?= v2.1.1
RELEASE_NAME = fast-web
DOCKERHUB_USER = tyvek2zhang
SOURCE_DIR = src
BUILD_DIR = build
DOCS_DIR = docs
SERVER_LOG = fast-web.log

help:
	@echo "Available make targets:"
	@echo "  install               Install project dependencies using uv"
	@echo "  db                    Generate db structure"
	@echo "  dp                    Upgrade db structure"
	@echo "  dev                   Development environment startup"
	@echo "  start                 Production environment startup"
	@echo "  lint                  Perform static code analysis"
	@echo "  test                  Run unit tests"
	@echo "  image                 Build the Docker image for the project"
	@echo "  push                  Push Docker image to dockerHub"
	@echo "  docker-compose-start  Start the project using Docker Compose"
	@echo "  deploy-k8s            Deploy the project to Kubernetes"
	@echo "  doc                   Generate documentation"
	@echo "  pypi                  Build and publish to PyPI"
	@echo "  clean                 Remove temporary files"
	@echo ""
	@echo "Use 'make <target>' to run a specific command."

install:
	uv sync

db:
	uv run alembic revision --autogenerate

dp:
	uv run alembic upgrade head

dev: install
	uv run alembic upgrade head && \
	uv run apiserver.py

start: install
	uv run alembic upgrade head && \
	nohup uv run apiserver.py --env prod > $(SERVER_LOG) 2>&1 &

lint:
	uv add pre-commit --group dev && \
	uv run pre-commit run --all-files --verbose

test: clean
	uv sync --group dev && \
	uv run alembic upgrade head && \
	cd $(SOURCE_DIR) && \
	uv run coverage run -m pytest tests && \
	uv run coverage html

ifeq ($(OS),Windows_NT)
clean:
	@echo "Cleaning on Windows..."
	@if exist dist rmdir /s /q dist 2>nul || echo "dist not found, skipping"
	@if exist $(DOCS_DIR)\build rmdir /s /q $(DOCS_DIR)\build 2>nul
	@if exist $(SOURCE_DIR)\htmlcov rmdir /s /q $(SOURCE_DIR)\htmlcov 2>nul
	@if exist $(SOURCE_DIR)\.coverage del /q $(SOURCE_DIR)\.coverage 2>nul
	@if exist $(SOURCE_DIR)\log rmdir /s /q $(SOURCE_DIR)\log 2>nul
	@if exist $(SOURCE_DIR)\tests\log rmdir /s /q $(SOURCE_DIR)\tests\log 2>nul

else
clean:
	rm -rf dist \
	    $(DOCS_DIR)/build \
	    $(SOURCE_DIR)/htmlcov \
	    $(SOURCE_DIR)/.coverage \

endif

image: clean
	docker build -t $(DOCKERHUB_USER)/$(RELEASE_NAME):$(TAG) .

push: image
	docker push $(DOCKERHUB_USER)/$(RELEASE_NAME):$(TAG)

docker-compose-start:
	cd $(BUILD_DIR) && docker-compose up -d

deploy-k8s:
	kubectl apply -f $(BUILD_DIR)/k8s

doc:
	uv add -r $(DOCS_DIR)/requirements.txt --group docs
	uv run sphinx-build -M html $(DOCS_DIR)/source/ $(DOCS_DIR)/build/

pypi:
	uv build
	uv publish
