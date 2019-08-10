.PHONY: all $(MAKECMDGOALS)

SHELL=/bin/bash

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# Build container for Django
django:
	docker build -f backend/Dockerfile -t mancelot backend

# Restart the backend
django-restart:
	git pull
	docker build -f backend/Dockerfile -t mancelot backend
	docker-compose -f backend/docker-compose.yml stop django celery celery-beat celery-flower
	docker-compose -f backend/docker-compose.yml rm -f django celery celery-beat celery-flower
	docker-compose -f backend/docker-compose.yml up -d
