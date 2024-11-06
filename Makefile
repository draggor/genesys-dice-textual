ifneq (,$(wildcard ./.env))
    include .env
    export
endif

PYTHON_VERSION ?= python3

clean:
	rm -rf ./build ./dist

build:
	uvx pyinstaller -p ./.venv/lib/python3.12/site-packages/ --onefile --add-data src/genesys_dice/tui/app.tcss:genesys_dice/tui --hidden-import textual.widgets._tab_pane -n genesys-dice src/genesys_dice/cli.py

build-win:
	uvx pyinstaller -p ./.venv/lib/site-packages/ --onefile --add-data ./src/genesys_dice/tui/app.tcss:genesys_dice/tui --hidden-import textual.widgets._tab_pane -n genesys-dice ./src/genesys_dice/cli.py

docs:
	uv run pdoc --html -o site genesys_dice

docs-serve:
	uv run python -m http.server -d site/genesys_dice

tui:
	uv run src/genesys_dice/cli.py

mypy:
	uv run mypy

.PHONY: clean build build-win mypy tui

