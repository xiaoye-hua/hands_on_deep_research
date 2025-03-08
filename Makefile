.PHONY: help install test lint format clean docs coverage pre-commit run test-tools test-python-runner test-code-agent coverage-code-agent

# Default target
help:
	@echo "Available commands:"
	@echo "  make help               - Show this help message"
	@echo "  make install            - Install dependencies"
	@echo "  make test               - Run all tests"
	@echo "  make test-tools         - Run tests for tools only"
	@echo "  make test-python-runner - Run tests for PythonRunner only"
	@echo "  make lint               - Run linting checks"
	@echo "  make format             - Format code"
	@echo "  make clean              - Clean build artifacts"
	@echo "  make docs               - Build documentation"
	@echo "  make coverage           - Run tests with coverage"
	@echo "  make pre-commit         - Run pre-commit hooks"
	@echo "  make run                - Run the application"
	@echo "  make test-code-agent    - Run tests for CodeAgent"
	@echo "  make coverage-code-agent - Run coverage for CodeAgent"

# Install dependencies
install:
	poetry install

# Run tests
test:
	poetry run pytest

# Run tests for tools only
test-tools:
	poetry run pytest tests/unit/tool/

# Run tests for PythonRunner only
test-python-runner:
	poetry run pytest tests/unit/tool/test_python_runner.py

# Run linting
lint:
	poetry run black --check src tests
	poetry run isort --check src tests
	poetry run mypy src tests
	poetry run pylint src tests

# Format code
format:
	poetry run black src tests
	poetry run isort src tests

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build documentation
docs:
	cd docs && poetry run sphinx-build -b html . _build/html

# Run tests with coverage
coverage:
	poetry run pytest --cov=src --cov-report=term --cov-report=html tests/

# Run tests with coverage for specific modules
coverage-tools:
	poetry run pytest --cov=src.tool --cov-report=term --cov-report=html tests/unit/tool/

# Run pre-commit hooks
pre-commit:
	poetry run pre-commit run --all-files

# Run the application
run:
	poetry run python -m src 

# Run tests for CodeAgent
test-code-agent:
	@echo "Running tests for CodeAgent..."
	python -m unittest tests/unit/agent/test_code_agent.py

# Run coverage for CodeAgent
coverage-code-agent:
	@echo "Running coverage for CodeAgent..."
	python -m coverage run -m unittest tests/unit/agent/test_code_agent.py
	python -m coverage report -m 