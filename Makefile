# Version is set in the pyproject.toml file
VERSION := $(shell grep -E "^version = " pyproject.toml | cut -d '"' -f2)
CWD := $(shell pwd)
PYTHON_VERSION := 3.12

# Commands
FORMAT := ruff format
CHECK := ruff check 
PYTHON := python3
RUN_UNIT_TESTS := $(PYTHON) -m pytest


.PHONY: debug, help, clear_cache, build_module, unittests, review, test

debug:
	@echo "ps-banshee" $(VERSION)
	@echo $(shell uv pip list | grep psengine)
	@echo "venv: $(shell which banshee)"
	

help:
	@echo "Available targets:"
	@echo " debug       - display debug information"
	@echo " test        - run review and unittests"
	@echo " unittests   - run  unittests"
	@echo " format      - run ruff format"
	@echo " syntaxfix   - run ruff check --fix"
	@echo " rev		    - run ruff check --fix and ruff format"
	@echo " review      - run ruff check and ruff format"
	@echo " build       - build python package"
	@echo "Miscellaneous targets:"
	@echo " clear_cache - remove python pycache and pytest_cache"

##########################################
#
# Targets related to development environment setup
#
##########################################
setup:
	uv venv --python $(PYTHON_VERSION)
	uv pip install -e ".[dev,docs]"
	@echo "Run > source .venv/bin/activate"

##########################################
#
# Targets related to build
#
##########################################
build: clear_cache format build_module clear_cache

build_module:
	uv build

##########################################
#
# Targets related to testing
#
##########################################
test: review unittests

unittests:
	$(RUN_UNIT_TESTS) -s --cov=banshee --cov-report html --cov-branch --cov-report term
	@coverage html


##########################################
#
# Targets related to code review
#
##########################################
review: format_check syntax
rev: format syntaxfix

FOLDERS=banshee tests

format:
	@$(FORMAT) $(FOLDERS)

format_check:
	@$(FORMAT) $(FOLDERS) --check

syntax:
	@$(CHECK) $(FOLDERS)

syntaxfix:
	@$(CHECK) $(FOLDERS) --fix

##########################################
#
# Misc targets
#
##########################################
clear_cache:
	find ./banshee -type d -name "__pycache__" -exec rm -rf {} \; 2>/dev/null || true
	rm -rf tests/__pycache__
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
