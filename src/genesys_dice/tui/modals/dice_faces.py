from typing import Any, Optional

from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.events import Click, Key
from textual.widgets import Static

from genesys_dice.tui.rich import get_faces_table


class DiceFacesModal(ModalScreen[Any]):
    DEFAULT_CSS = """
    DiceFacesModal {
        align: center middle;

        Static {
            padding: 0 1;
            width: auto;
            content-align: center middle;
            border: thick $background 80%;
        }
    }
    """

    def compose(self) -> ComposeResult:
        yield Static(get_faces_table())

    def check_consume_key(self, key: str, character: Optional[str]) -> bool:
        """
        Always return True for every key to close the modal.
        This is what it takes to override priority bindings
        such as the command_palette
        """
        return True

    @on(Click)
    @on(Key)
    def dismiss_click(self, event: Click | Key) -> None:
        event.stop()
        self.dismiss()
