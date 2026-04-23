.PHONY: help install dev test lint format clean

help:
	@echo "devkit - Modern Developer Workflow CLI"
	@echo ""
	@echo "Commands:"
	@echo "  make install     Install devkit"
	@echo "  make dev         Install in development mode"
	@echo "  make test        Run tests"
	@echo "  make lint        Check code quality"
	@echo "  make format      Format code"
	@echo "  make clean       Clean up build artifacts"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

test-integration:
	python test_integration.py

lint:
	black --check src/ tests/
	ruff check src/ tests/
	mypy src/ --ignore-missing-imports

format:
	black src/ tests/
	ruff check --fix src/ tests/

clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/ .coverage htmlcov/
