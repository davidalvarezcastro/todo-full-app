.PHONY: help
.DEFAULT:= help
SHELL := /bin/bash

help: ## Command list with description    
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install_dependencies: ## Install pyproject.toml dependencies
	poetry install --no-root

dev:  ## Deploy Fast Api App
	docker compose up --build -d

deploy_test_db: ## Create a testing database
	docker compose --env-file .env.testing -f docker-compose.testing.yml up --build -d

run_tests: ## Run all tests
	poetry run pytest tests
