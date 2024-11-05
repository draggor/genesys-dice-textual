from collections.abc import Callable
from typing import Any

from textual.app import App
from textual.widgets import TabbedContent


def switch_tab(tab: str, app: App) -> Callable[[Any], None]:
    def inner(modal_return: Any = None) -> None:
        app.set_focus(None)
        app.query_one(TabbedContent).active = tab

    return inner
