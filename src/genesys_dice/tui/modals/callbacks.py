from collections.abc import Callable
from typing import Optional, TypeVar

from textual.app import App
from textual.widgets import TabbedContent

from genesys_dice.dice import DicePool

T = TypeVar("T")


def switch_tab(tab_str: str, app: App, tab_class=None) -> Callable[[T], None]:
    U = TypeVar("U")

    def inner(modal_return: Optional[U] = None) -> None:
        if modal_return is not None:
            app.set_focus(None)
            tab = app.query_one(TabbedContent)
            tab.active = tab_str

            if tab_class is None:
                raise Exception(
                    "tab_class parameter required if accepting data from modal"
                )

            if tab.active_pane:
                destination_tab = tab.active_pane.query_one(tab_class)
                destination_tab.set_data(modal_return)

    return inner


SavedRollFn = Callable[[Optional[DicePool]], None]
