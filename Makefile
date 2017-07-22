PYTHON=python3

PIP=venv/bin/python -m pip
FLAKE=venv/bin/flake8
PYTEST=venv/bin/py.test

.PHONY: help clean delpyc install install-dev tests flake quality

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  delpyc              -- to remove all *.pyc files, this is recursive from the current directory"
	@echo "  clean               -- to clean local repository from all stuff created during development"
	@echo
	@echo "  flake               -- to launch Flake8 checking on code"
	@echo "  tests               -- to launch tests using py.test"
	@echo "  quality             -- to launch Flake8 checking and tests with py.test"
	@echo

delpyc:
	find . -name "*\.pyc"|xargs rm -f

clean: delpyc
	rm -Rf venv dist .tox Optimus.egg-info .cache docs/_build

venv:
	$(PYTHON) -m venv venv

install: venv
	$(PIP) install -e .

install-dev: install
	$(PIP) install -r requirements/dev.txt

flake:
	$(FLAKE) --show-source crispy_forms_foundation

tests:
	$(PYTEST) -vv tests/

quality: tests flake