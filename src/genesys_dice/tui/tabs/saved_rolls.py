from collections.abc import Callable
from typing import Optional, List

from rich.pretty import Pretty

from textual import on, events
from textual.app import ComposeResult
from textual.containers import Center, Container, Grid, Horizontal
from textual.reactive import reactive
from textual.widgets import Placeholder, Label, Static, Button, RichLog

from genesys_dice import data
from genesys_dice.tui.widgets.button_plus import ButtonPlus


class Roll(Container, can_focus=True):
    DEFAULT_CSS = """
    Roll {
        width: auto;
        height: auto;
        border: solid white;
        content-align: center middle;
        background: $primary-background-darken-1;

        &:focus {
            border: thick white;
        }

        /*
        &.-hover {
            background: black;
        }

        &.-hover Label {
            background: black;
        }

        &:focus {
            border: thick white;
        }
        */

        Horizontal {
            width: auto;
            height: auto;

            Label {
                width: auto;
                height: auto;
                border: solid white;
                background: red;
            }
        }

    }

    """

    # saved_roll: reactive[SavedRoll] = reactive(SavedRoll, recompose=True)
    roll: data.SavedRoll

    def __init__(self, roll: data.SavedRoll, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.roll = roll
        self.border_title = roll.name

    def compose(self) -> ComposeResult:
        # with Center():
        #    yield Static(self.roll.name)
        with Horizontal():
            yield Label("And more text Dice: ")
            yield Label(self.roll.dice)

    # @on(events.Enter)
    # @on(events.Leave)
    # def on_enter(self, event: events.Enter):
    #    event.stop()
    #    self.set_class(self.is_mouse_over, "-hover")


class HoverButton(Button):
    DEFAULT_CSS = """
    HoverButton {
        width: auto;
        content-align: center middle;
        &.-hover {
            border-top: tall $panel;
            background: $panel-darken-2;
        }
        &.-hover * {
            background: $panel-darken-2;
        }

        &.-active {
            background: $panel;
            border-bottom: tall $panel-lighten-2;
            border-top: tall $panel-darken-2;
            tint: $background 30%;
        }

        &.-active * {
            background: $panel;
            tint: $background 30%;
        }

        &> * {
            content-align: center middle;
        }
    }
    """

    def get_content_width(self, container, viewport) -> int:
        return self.query_children().first().get_content_width(container, viewport) + 2

    @on(events.Enter)
    @on(events.Leave)
    def on_enter(self, event: events.Enter):
        event.stop()
        self.set_class(self.is_mouse_over, "-hover")


class RollGrid(Container):
    DEFAULT_CSS = """
    RollGrid {
        layout: grid;
        grid-size: 2;
        grid-gutter: 1;
        grid-rows: auto;
        grid-columns: auto;
    }
    """

    saved_rolls: reactive[List[data.SavedRoll]] = reactive(list, recompose=True)
    display = ""

    def compose(self) -> ComposeResult:
        hover_button = HoverButton()
        styles = hover_button.styles
        # self.display = Pretty(styles, expand_all=True)
        rich_log = RichLog()
        rich_log.write(styles)

        for roll in self.saved_rolls:
            # yield Roll(roll)
            with HoverButton(""):
                with Center():
                    yield Roll(roll)

        with hover_button:
            yield Static("did it work?")

        # yield RichLog(id="--styles")


class SavedRolls(Container):

    saved_rolls: reactive[List[data.SavedRoll]] = reactive(list, always_update=True)

    def compose(self) -> ComposeResult:
        yield RollGrid(id="RollGrid").data_bind(SavedRolls.saved_rolls)

    def add_roll(self, roll: data.SavedRoll) -> None:
        self.saved_rolls.append(roll)
        self.mutate_reactive(SavedRolls.saved_rolls)

    def set_data(self, roll: Optional[data.SavedRoll] = None) -> None:
        if roll is not None:
            self.add_roll(roll)
