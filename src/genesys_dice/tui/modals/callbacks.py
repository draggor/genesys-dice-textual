from collections.abc import Callable
from typing import Optional

from textual.app import App
from textual.widgets import TabbedContent

from genesys_dice.data import SavedRoll


def switch_tab[T, V](tab_str: str, app: App, tab_class) -> Callable[[T], None]:
    def inner[U](modal_return: Optional[U] = None) -> None:
        if modal_return is not None:
            app.set_focus(None)
            tab = app.query_one(TabbedContent)
            tab.active = tab_str
            # TODO: this is fucky and there technically can be Nones
            #       and making mypy happy on top of that is ???
            #       Probably a code smell anyway.
            if tab.active_pane:
                children = tab.active_pane.query_children()
                if len(children) > 0:
                    destination_tab = children.first(tab_class)
                    destination_tab.set_data(modal_return)

    return inner


type SavedRollFn = Callable[[Optional[SavedRoll]], None]
