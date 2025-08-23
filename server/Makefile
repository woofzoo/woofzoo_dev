# Makefile for WoofZoo FastAPI Project

.PHONY: help install install-dev run test test-cov lint format type-check clean db-init db-migrate db-upgrade db-downgrade

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  run          - Run the development server"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with black and isort"
	@echo "  type-check   - Run type checking with mypy"
	@echo "  clean        - Clean up cache files"
	@echo "  db-init      - Initialize database"
	@echo "  db-migrate   - Create a new migration"
	@echo "  db-upgrade   - Apply database migrations"
	@echo "  db-downgrade - Rollback database migrations"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"

# Development
run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=app --cov-report=html --cov-report=term-missing

# Code quality
lint:
	flake8 app/ tests/
	black --check app/ tests/
	isort --check-only app/ tests/

format:
	black app/ tests/
	isort app/ tests/

type-check:
	mypy app/

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage

# Database
db-init:
	alembic init alembic

db-migrate:
	alembic revision --autogenerate -m "$(message)"

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

# Docker (if needed)
docker-build:
	docker build -t woofzoo .

docker-run:
	docker run -p 8000:8000 woofzoo

# Quick setup for new developers
setup: install-dev db-upgrade
	@echo "Setup complete! Run 'make run' to start the development server."
