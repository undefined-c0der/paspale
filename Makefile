# Makefile for paspale development

.PHONY: install dev test lint format clean docs

# Install package
install:
	pip install -e .

# Install with dev dependencies
dev:
	pip install -e ".[dev]"

# Run tests
test:
	pytest tests/ -v

# Run tests with coverage
coverage:
	pytest tests/ -v --cov=paspale --cov-report=html

# Lint code
lint:
	mypy src/paspale
	black --check src/paspale tests
	isort --check-only src/paspale tests

# Format code
format:
	black src/paspale tests examples
	isort src/paspale tests examples

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf src/*.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build package
build: clean
	python -m build

# Upload to PyPI (test)
upload-test: build
	twine upload --repository testpypi dist/*

# Upload to PyPI
upload: build
	twine upload dist/*
