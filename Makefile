ifneq (,$(wildcard ./.env))
    include .env
    export
endif

PYTHON_VERSION ?= python3

clean:
	rm -rf ./build ./dist

build:
	uvx pyinstaller -p ./.venv/lib/python3.12/site-packages/ --onefile -n genesys-dice src/cli.py

dice:
	uv run src/cli.py

tui:
	uv run src/tui.py

mypy:
	uv run mypy

.PHONY: clean build dice mypy tui

