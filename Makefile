.PHONY: help
.DEFAULT:= help
NAME := todoapp
SHELL := /bin/bash

help: ## Command list with description    
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

# BACKEND
install_backend_dependencies: ## Install pyproject.toml dependencies
	cd backend && poetry install --no-root

deploy_test_db: ## Create a testing database
	docker compose --env-file ./backend/.env.testing -f docker-compose.testing.yml up --build -d

run_tests: ## Run all tests
	cd backend && poetry run pytest tests

# DEV
build_backend_dev: ## Compila imagen para backend
	@docker build -t $(NAME)_backend_dev --target local -f ./backend/Dockerfile ./backend

build_frontend_dev: ## Compila imagen para frontend
	@docker build -t $(NAME)_frontend_dev --target dev -f ./web/Dockerfile ./web

dev:  ## Deploy TodoApp (dev mode)
	docker compose up --build
