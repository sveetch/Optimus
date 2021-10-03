PYTHON_INTERPRETER=python3
VENV_PATH=.venv
PIP=$$(VENV_PATH)/bin/pip
OPTIMUS=$$(VENV_PATH)/bin/optimus-cli
PROJECT_DIR=project/
SETTINGS_BASE=settings.base
SETTINGS_PROD=settings.production
SERVER_HOST="0.0.0.0:8001"


help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  install             -- to install this project with virtualenv and Pip"
	@echo ""
	@echo "  clean-pycache       -- to remove all __pycache__, this is recursive from current directory"
	@echo "  clean-builds        -- to remove everything builded by Optimus (pages, statics, etc..)"
	@echo "  clean               -- to clean local repository from all stuff created during development"
	@echo ""
	@echo "  build               -- to build project with default environnement"
	@echo "  watch               -- to launch project watcher with default environnement"
	@echo "  server              -- to launch local server on $$(SERVER_HOST) with default environnement"
	@echo ""
	@echo "  build-prod          -- to build project with production environnement"
	@echo "  server-prod         -- to launch local server on $$(SERVER_HOST) with production environnement"
	@echo

clean-pycache:
	@echo ""
	@echo "==== Clear Python cache ===="
	@echo ""
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
.PHONY: clean-pycache

clean-builds:
	@echo ""
	@echo "==== Clear builds ===="
	@echo ""
	rm -Rf $$(PROJECT_DIR)/_build
	rm -Rf $$(PROJECT_DIR)/.webassets-cache
	rm -Rf $$(PROJECT_DIR)/locale/**/*.mo
	find locale -name "*\.mo"|xargs rm -f
.PHONY: clean-builds

clean-install:
	@echo ""
	@echo "==== Clear installation ===="
	@echo ""
	rm -Rf $$(VENV_PATH)
.PHONY: clean-install

clean: clean-install clean-builds clean-pycache
.PHONY: clean

venv:
	@echo ""
	@echo "==== Install virtual environment ===="
	@echo ""
	virtualenv -p $$(PYTHON_INTERPRETER) $$(VENV_PATH)
	# This is required for those ones using old distribution
	$$(PIP) install --upgrade pip
	$$(PIP) install --upgrade setuptools
.PHONY: venv

install: venv
	@echo ""
	@echo "==== Install everything ===="
	@echo ""
	$$(PIP) install -r requirements.txt
.PHONY: install

build:
	@echo ""
	@echo "==== Build for development environment ===="
	@echo ""
	$$(OPTIMUS) build --basedir $$(PROJECT_DIR) --settings-name $$(SETTINGS_BASE)
.PHONY: build

watch:
	@echo ""
	@echo "==== Launch watcher for development environment ===="
	@echo ""
	$$(OPTIMUS) watch --basedir $$(PROJECT_DIR) --settings-name $$(SETTINGS_BASE)
.PHONY: watch

server:
	@echo ""
	@echo "==== Run server for development environment ===="
	@echo ""
	$$(OPTIMUS) runserver --basedir $$(PROJECT_DIR) --settings-name $$(SETTINGS_BASE) $$(SERVER_HOST)
.PHONY: server

build-prod:
	@echo ""
	@echo "==== Build for production environment ===="
	@echo ""
	$$(OPTIMUS) build --basedir $$(PROJECT_DIR) --settings-name $$(SETTINGS_PROD)
.PHONY: build-prod

server-prod:
	@echo ""
	@echo "==== Run server for production environment ===="
	@echo ""
	$$(OPTIMUS) runserver --basedir $$(PROJECT_DIR) --settings-name $$(SETTINGS_PROD) $$(SERVER_HOST)
.PHONY: server-prod
