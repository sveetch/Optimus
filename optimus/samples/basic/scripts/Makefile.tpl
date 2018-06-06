PYTHON=python3

PIP=venv/bin/pip
OPTIMUS=venv/bin/optimus-cli

.PHONY: help clean delpyc install

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  install             -- to install this project with virtualenv and Pip"
	@echo ""
	@echo "  delpyc              -- to remove all __pycache__, this is recursive from current directory"
	@echo "  clean               -- to clean local repository from all stuff created during development"
	@echo ""
	@echo "  build               -- to build project with default environnement"
	@echo "  watch               -- to launch project watcher with default environnement"
	@echo ""
	@echo "  build-prod          -- to build project with production environnement"
	@echo

delpyc:
	find . -type d -name "__pycache__"|xargs rm -Rf

clean: delpyc
	rm -Rf venv

venv:
	virtualenv -p $$(PYTHON) venv
	# This is required for those ones using ubuntu<16.04
	$$(PIP) install --upgrade pip
	$$(PIP) install --upgrade setuptools

install: venv
	$$(PIP) install -r requirements.txt

build:
	$$(OPTIMUS) build

watch:
	$$(OPTIMUS) watch

build-prod:
	$$(OPTIMUS) build --settings prod_settings
