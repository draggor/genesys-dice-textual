from collections.abc import Callable
from typing import Optional, List

from textual import on, events
from textual.app import ComposeResult
from textual.containers import Center, Container, Grid, Horizontal
from textual.reactive import reactive
from textual.widgets import Placeholder, Label, Static

from genesys_dice.data import SavedRoll


class Roll(Container, can_focus=True):
    DEFAULT_CSS = """
    Roll {
        width: auto;
        height: auto;
        border: solid white;
        content-align: center middle;
        background: $primary-background-darken-1;

        &.-hover {
            background: black;
        }

        /*
        .-hover {
            background: black;
        }
        */

        &:focus {
            border: thick white;
        }

        Horizontal {
            width: auto;
            height: auto;

            Label {
                width: auto;
                height: auto;
                border: solid white;
                background: red;

                &.-hover {
                    background: green;
                }
            }
        }

    }

    """

    # saved_roll: reactive[SavedRoll] = reactive(SavedRoll, recompose=True)
    roll: SavedRoll

    def __init__(self, roll: SavedRoll, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.roll = roll
        self.border_title = roll.name

    def compose(self) -> ComposeResult:
        # with Center():
        #    yield Static(self.roll.name)
        with Horizontal():
            yield Label("Dice: ")
            yield Label(self.roll.dice)

    @on(events.Enter)
    @on(events.Leave)
    def on_enter(self, event: events.Enter):
        event.stop()
        self.set_class(self.is_mouse_over, "-hover")

        for child in self.query():
            child.set_class(self.is_mouse_over, "-hover")


class RollGrid(Grid):
    DEFAULT_CSS = """
    RollGrid {
        layout: grid;
        grid-size: 2;
        grid-gutter: 1;
        grid-rows: auto;
        grid-columns: auto;
    }
    """

    saved_rolls: reactive[List[SavedRoll]] = reactive(list, recompose=True)

    def compose(self) -> ComposeResult:
        for roll in self.saved_rolls:
            yield Roll(roll)


class SavedRolls(Container):

    saved_rolls: reactive[List[SavedRoll]] = reactive(list, always_update=True)

    def compose(self) -> ComposeResult:
        yield RollGrid(id="RollGrid").data_bind(SavedRolls.saved_rolls)

    def add_roll(self, roll: SavedRoll) -> None:
        self.saved_rolls.append(roll)
        self.mutate_reactive(SavedRolls.saved_rolls)

    def set_data(self, roll: Optional[SavedRoll] = None) -> None:
        if roll is not None:
            self.add_roll(roll)
