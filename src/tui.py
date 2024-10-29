from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Placeholder

from dice import (
    roll,
    results_table,
    success_probability,
    dice_map,
    Dice,
    Die,
    dice_display,
    symbol_display,
)

from die_button import DieButton


class DiceMenu(Container):
    DEFAULT_CSS = """
    DiceMenu {
        height: 1fr;
        width: 1fr;
        layout: grid;
        grid-size: 7;
    }
    """

    def compose(self) -> ComposeResult:
        for die_type, die in dice_map.items():
            yield DieButton(die, id=die_type.name)


class Pending(Placeholder):
    DEFAULT_CSS = """
    Pending {
        height: 1fr;
        width: 1fr;
    }
    """


class Tray(Horizontal):
    def compose(self) -> ComposeResult:
        yield Pending(id="Pending")
        yield DiceMenu(id="DiceMenu")


class TrayScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header(id="Header")
        yield Tray(id="Tray")
        yield Footer(id="Footer")


class DiceApp(App):
    def on_mount(self) -> None:
        self.push_screen(TrayScreen())


if __name__ == "__main__":
    app = DiceApp()
    app.run()
