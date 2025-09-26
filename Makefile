#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = Agent Code
PYTHON_VERSION = 3.12
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################



uv_install:
	uv pip install --upgrade pip && \
		uv pip install -r pyproject.toml

install:
	pip install --upgrade pip && \
		pip install -r pyproject.toml

import_format:
	uv run isort src/

format:
	uv run black src/

ruff_format:
	uv run ruff format src/

lint:
	uv run pylint --disable=R,C src/

ruff_lint:
	uv run ruff check src/

typepyright:
	uv run pyright src/

typemypy:
	uv run mypy src/

typepyrefly:
	uv run pyrefly check src/

## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	@echo ">>> Creating virtual environment using uv..."
	uv venv --python $(PYTHON_VERSION)
	@echo ">>> Virtual environment created in .venv"
	@echo ">>> Activate it in your terminal with:"
	@echo ">>>   Windows: .\.venv\Scripts\activate"
	@echo ">>>   Unix/macOS: source ./.venv/bin/activate"
test:
	@echo ">>> Running tests with coverage..."
		uv run pytest

refactor: format lint

all: uv_install format lint typepyright typepyrefly import_format ruff_format ruff_lint test