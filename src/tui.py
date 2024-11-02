from dataclasses import field
from typing import Any, Dict, List, Tuple

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.message import Message
from textual.reactive import reactive
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
            yield DieButton(die, id=die_type.name, classes="tray")


class Pending(Horizontal):
    DEFAULT_CSS = """
    Pending {
        height: 1fr;
        width: 1fr;
    }
    """

    dice: List[Dice] = reactive(list, recompose=True)

    def compose(self) -> ComposeResult:
        for die_type in self.dice:
            die = dice_map[die_type]
            yield DieButton(die, id=die_type.name, classes="pending")

    def modify_dice(self, die: Die) -> None:
        self.dice.append(die.die_type)
        self.mutate_reactive(Pending.dice)


class Tray(Horizontal):
    def compose(self) -> ComposeResult:
        yield Pending(id="Pending")
        yield DiceMenu(id="DiceMenu")

    @on(Button.Pressed, ".tray")
    def modify_pending_dice(self, message: DieButton.Pressed) -> None:
        self.query_one(Pending).modify_dice(message.control.die)


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
