ifneq (,$(wildcard ./.env))
    include .env
    export
endif

PYTHON_VERSION ?= python3

clean:
	rm -rf ./build ./dist

build:
	uv run pyinstaller --onefile --add-data src/genesys_dice/tui/app.tcss:genesys_dice/tui --add-data src/genesys_dice/test-data.yaml:genesys_dice --hidden-import textual.widgets._tab_pane -n genesys-dice src/genesys_dice/cli.py

build-web:
	uv run pyinstaller --onefile --collect-data textual_serve -n genesys-dice-web src/genesys_dice/serve.py

build-win:
	uv run pyinstaller --onefile --add-data ./src/genesys_dice/tui/app.tcss:genesys_dice/tui --add-data ./src/genesys_dice/test-data.yaml:genesys_dice --hidden-import textual.widgets._tab_pane -n genesys-dice ./src/genesys_dice/cli.py

docs:
	uv run pdoc --html -o site genesys_dice

docs-serve:
	uv run python -m http.server -d site/genesys_dice

tui:
	uv run src/genesys_dice/cli.py

mypy:
	uv run mypy

.PHONY: clean build build-web build-win mypy tui

