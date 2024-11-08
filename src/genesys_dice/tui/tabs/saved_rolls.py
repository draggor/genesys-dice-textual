from collections.abc import Callable
from dataclasses import asdict
from typing import Optional, List

from textual import on, events
from textual.app import ComposeResult
from textual.containers import (
    Center,
    Container,
    Grid,
    Horizontal,
    ScrollableContainer,
    ItemGrid,
)
from textual.geometry import Size
from textual.reactive import reactive
from textual.widgets import Placeholder, Label, Static, Button, RichLog

from genesys_dice import data
from genesys_dice.dice import DicePool, get_dice_from_str
from genesys_dice.tui.widgets.button_plus import ButtonPlus
from genesys_dice.tui.widgets.die_button import DieButton


class Roll(Container):
    DEFAULT_CSS = """
    Roll {
        width: 100%;
        height: auto;
        border: solid white;
        margin: 0 1;
        content-align: center middle;
        background: $primary-background-darken-1;

        Horizontal {
            width: auto;
            height: auto;
            content-align: center middle;

            #-roll-label {
                width: auto;
                min-width: 9;
                height: auto;
                margin: 1;
                padding: 1 0;
                background: $primary-background-lighten-1;
                text-align: center;

                &:hover {
                    background: $primary-background-lighten-1;
                }
            }
        }

        #-roll-description {
            margin: 0 1;
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
            with Horizontal():
                yield Label("Dice: ", id="-roll-label")
                # for die_type in get_dice_from_str(self.roll.dice):
                for die_type in self.roll.get_dice():
                    yield DieButton(die_type, disabled=True)
        if self.roll.description is not None:
            yield Static(self.roll.description, id="-roll-description")

    def get_content_width(self, container: Size, viewport: Size) -> int:
        orig: int = super().get_content_width(container, viewport)
        return max(orig, len(self.border_title) + 6)


class RollGrid(ScrollableContainer):
    DEFAULT_CSS = """
    RollGrid {
        layout: grid;
        grid-size: 2;
        grid-gutter: 1;
        grid-rows: auto;

        .-grid-button {
            height: 100%;
        }
    }
    """

    saved_rolls: reactive[List[DicePool]] = reactive(list, recompose=True)

    def compose(self) -> ComposeResult:
        for idx, roll in enumerate(self.saved_rolls):
            with ButtonPlus("", id=f"-button-{idx}", classes="-grid-button"):
                with Center():
                    yield Roll(roll)

    # TODO: figure out how to solve the equal Roll border box size issue
    #       This doesn't work, onlyhappens once, adding a widget after breaks it.
    # def on_show(self) -> None:
    #    two = []
    #    for box in self.query(Roll):
    #        two.append(box)

    #        if len(two) == 2:
    #            height = max(two[0].content_size.height, two[1].content_size.height) + 2
    #            two[0].styles.height = height
    #            two[1].styles.height = height
    #            two = []


class SavedRolls(Container):

    saved_rolls: reactive[List[DicePool]] = reactive(list, always_update=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.saved_rolls = data.load_from_file("test-data.yaml")

    def compose(self) -> ComposeResult:
        yield RollGrid(id="RollGrid").data_bind(SavedRolls.saved_rolls)

    def add_roll(self, roll: DicePool) -> None:
        self.saved_rolls.append(roll)
        self.mutate_reactive(SavedRolls.saved_rolls)

    def set_data(self, roll: Optional[DicePool] = None) -> None:
        if roll is not None:
            self.notify(str(roll.asdict()))
            self.add_roll(roll)
