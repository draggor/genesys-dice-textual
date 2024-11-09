from collections.abc import Callable
from dataclasses import asdict
from typing import Optional, List

from textual import on, events
from textual.app import ComposeResult
from textual.containers import (
    Center,
    Container,
    Horizontal,
    ItemGrid,
    ItemGrid,
    Middle,
    Vertical,
    VerticalGroup,
    VerticalScroll,
)
from textual.geometry import Size
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Placeholder, Label, Static, Button, RichLog, TextArea

from genesys_dice import data
from genesys_dice.dice import DicePool, get_dice_from_str
from genesys_dice.tui.widgets.die_button import DieButton


class Roll(Vertical, can_focus=True, can_focus_children=False):
    DEFAULT_CSS = """
    Roll {
        width: 1fr;
        height: auto;
        padding: 1 1 0 1;
        border: solid white;
        background: $panel;
        color: $text;
        text-align: center;
        text-style: bold;
        box-sizing: border-box;

        &:focus {
            border: tall white;
            border-title-color: $text;
            background: $primary-background-lighten-3 40%;
            opacity: 1.0;
        }

        &.-hover {
            background: $primary 60%;
            opacity: 1.0;
        }

        #-dice-container {
            width: auto;
            height: 3;
        }

        .-button-display {
            margin: 0 1;

            &:disabled {
                opacity: 1;
            }
        }

        #-roll-description {
            margin: 1 0 0 0;
        }
    }
    """

    roll: reactive[DicePool] = reactive(DicePool)

    def __init__(self, roll: DicePool, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.roll = roll
        self.border_title: str = roll.name

    def compose(self) -> ComposeResult:
        with Center():
            with Horizontal(id="-dice-container"):
                for die_type in self.roll.get_dice():
                    yield DieButton(die_type, disabled=True, classes="-button-display")
        yield Static(self.roll.description, id="-roll-description")

    @on(events.Enter)
    @on(events.Leave)
    def on_enter(self, event: events.Enter):
        event.stop()
        self.set_class(self.is_mouse_over, "-hover")


class SavedRolls(Vertical):
    DEFAULT_CSS = """
    SavedRolls {
        align-horizontal: center;
        ItemGrid {
            margin: 0 1 0 0;
            padding: 0;
            background: $boost;
            width: 1fr;
            height: auto;
            grid-gutter: 0;
            grid-rows: auto;
        }
    }
    """

    saved_rolls: reactive[List[DicePool]] = reactive(
        list, always_update=True, recompose=True
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.saved_rolls = data.load_from_file("test-data.yaml")

    def compose(self) -> ComposeResult:
        with VerticalScroll() as container:
            container.can_focus = False
            with ItemGrid(min_column_width=32):
                for roll in self.saved_rolls:
                    yield Roll(roll)

    def add_roll(self, roll: DicePool) -> None:
        self.saved_rolls.append(roll)
        self.mutate_reactive(SavedRolls.saved_rolls)

    def set_data(self, roll: Optional[DicePool] = None) -> None:
        if roll is not None:
            self.add_roll(roll)
