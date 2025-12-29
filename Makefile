.PHONY: help install test clean build

help:
	@echo "AntPorter - Available Commands"
	@echo "=============================="
	@echo "install      - Install package"
	@echo "test         - Run tests"
	@echo "clean        - Clean build artifacts"
	@echo "build        - Build distribution"

install:
	@pip install -e .

test:
	@pytest -v

clean:
	@rm -rf build/ dist/ *.egg-info src/*.egg-info
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.part*" -delete
	@find . -type f -name "*.meta.json" -delete

build: clean
	@python -m build
