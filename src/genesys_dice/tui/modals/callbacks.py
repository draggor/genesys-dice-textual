from collections.abc import Callable
from typing import Optional

from textual.app import App
from textual.widgets import TabbedContent

from genesys_dice.dice import DicePool


def switch_tab[T](tab_str: str, app: App, tab_class=None) -> Callable[[T], None]:
    def inner[U](modal_return: Optional[U] = None) -> None:
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


type SavedRollFn = Callable[[Optional[DicePool]], None]
