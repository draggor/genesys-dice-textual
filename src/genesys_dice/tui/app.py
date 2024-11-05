import pyperclip  # type: ignore

from rich.text import Text

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.message import Message
from textual.screen import Screen
from textual.widgets import (
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
    def on_mount(self) -> None:
        self.push_screen(AppScreen())

    # def action_change_tab(self, tab_id: str) -> None:
    #    self.notify("action")
    #    self.query_one(TabbedContent).active = tab_id


if __name__ == "__main__":
    app = DiceApp()
    app.run()
