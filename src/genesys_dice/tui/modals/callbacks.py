from collections.abc import Callable
from typing import Optional

from textual.app import App
from textual.widgets import TabbedContent

from genesys_dice.data import SavedRoll


def switch_tab[T](tab_str: str, app: App) -> Callable[[T], None]:
    def inner[U](modal_return: Optional[U] = None) -> None:
        if modal_return is not None:
            app.set_focus(None)
            tab = app.query_one(TabbedContent)
            tab.active = tab_str
            # TODO: this is fucky and there technically can be Nones
            #       and making mypy happy on top of that is ???
            #       Probably a code smell anyway.
            tab.active_pane.query_children().first().set_data(modal_return)

    return inner


type SavedRollFn = Callable[[Optional[SavedRoll]], None]


def switch_tab_saved_roll(
    tab_str: str, app: App
) -> Callable[[Optional[SavedRoll]], None]:
    """
    This is a convenience method so that other modules don't have to
    fill out the full type signature, which is pretty messy.
    """
    callback: Callable[[Optional[SavedRoll]], None] = switch_tab(tab_str, app)
    return callback
