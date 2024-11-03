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
    Modifier,
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
        for die_type in dice_display.keys():
            die = dice_map[die_type]
            yield DieButton(die, id=die_type.name, classes="tray")


class Pending(Container):
    DEFAULT_CSS = """
    Pending {
        height: 1fr;
        width: 1fr;
    }
    """

    @staticmethod
    def default_dice() -> Dict[Dice, int]:
        d = {}

        for die_type in dice_display.keys():
            d[die_type] = 0

        return d

    dice: reactive[Dict[Dice, int]] = reactive(default_dice, recompose=True)

    def compose(self) -> ComposeResult:
        css_id: int = 0

        for die_type, count in self.dice.items():
            die = dice_map[die_type]
            row = []
            for _ in range(1, count + 1):
                css_id += 1
                row.append(
                    DieButton(die, id=f"{die_type.name}{css_id}", classes="pending")
                )

            yield Horizontal(*row)

    def modify_dice(self, die: Die) -> None:
        self.dice[die.die_type] += 1
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
