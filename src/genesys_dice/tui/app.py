from typing import Optional

import pyperclip  # type: ignore

from rich.text import Text

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.message import Message
from textual.screen import Screen
from textual.widgets import (
    Button,
    Header,
    Footer,
    Placeholder,
    TabbedContent,
    TabPane,
)

from genesys_dice.tui.messages import ModalMessage
from genesys_dice.tui.tabs import Tray, Templates


class AppScreen(Screen):
    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield Header(id="Header")

        with TabbedContent(initial="tray-tab"):
            with TabPane("Dice Tray", id="tray-tab"):
                yield Tray(id="Tray")
            with TabPane("Templates", id="template-tab"):
                yield Templates(id="Templates")

        yield Footer(id="Footer")


class DiceApp(App):

    starting_dice: Optional[str] = None

    def __init__(self, dice_str: Optional[str] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.starting_dice = dice_str

    async def on_mount(self) -> None:
        await self.push_screen(AppScreen())
        if self.starting_dice is not None:
            self.query_one(Tray).set_dice(self.starting_dice)
            # self.query_one("#Save", Button).press()


if __name__ == "__main__":
    app = DiceApp()
    app.run()
