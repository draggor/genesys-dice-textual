from collections.abc import Callable
from typing import Optional, List

from textual import on, events
from textual.app import ComposeResult
from textual.containers import (
    Center,
    Horizontal,
    ItemGrid,
    Vertical,
    VerticalScroll,
)
from textual.reactive import reactive
from textual.widgets import (
    Static,
    TabPane,
)

from genesys_dice import data
from genesys_dice.dice import DicePool
from genesys_dice.tui.messages import SwitchTabMessage
from genesys_dice.tui.widgets.die_button import DieButton
from genesys_dice.tui.tabs.data_tab import DataTab


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

    BINDINGS = (("enter", "send_roll_to_tray()", "Send roll to tray"),)

    dice: reactive[DicePool] = reactive(DicePool)

    def __init__(self, dice: DicePool, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dice = dice
        self.border_title: str = dice.name

    def compose(self) -> ComposeResult:
        with Center():
            with Horizontal(id="-dice-container"):
                for die_type in self.dice.get_dice():
                    yield DieButton(die_type, disabled=True, classes="-button-display")
        yield Static(self.dice.description, id="-roll-description")

    def action_send_roll_to_tray(self) -> None:
        self.app.set_focus(None)
        self.post_message(SwitchTabMessage("tray-tab", self.dice))

    @on(events.Enter)
    @on(events.Leave)
    def on_enter(self, event: events.Enter):
        event.stop()
        self.set_class(self.is_mouse_over, "-hover")

    @on(events.Click)
    def handle_click(self, event: events.Click):
        """
        A widget becomse focused on mouse_down right away.
        We use -activated class to check if we're ready
        to send the roll to the tray, aka, need to click twice.
        """
        event.stop()
        if self.is_mouse_over and self.has_class("-activated"):
            self.action_send_roll_to_tray()
        else:
            self.add_class("-activated")

    @on(events.Blur)
    def handle_unfocus(self):
        self.remove_class("-activated")


class SavedRolls(TabPane, DataTab[DicePool], can_focus=True):
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
    next_show_cb: Optional[Callable] = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.saved_rolls = data.load_from_file("test-data.yaml")

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="-scroll-window") as container:
            container.can_focus = False
            with ItemGrid(id="-item-grid", min_column_width=32):
                for roll in self.saved_rolls:
                    yield Roll(roll)

    def on_show(self, event):
        if self.next_show_cb is not None:
            self.next_show_cb()
            self.next_show_cb = None

    def add_roll(self, roll: DicePool) -> None:
        self.saved_rolls.append(roll)
        self.mutate_reactive(SavedRolls.saved_rolls)

    def set_data(self, roll: Optional[DicePool] = None) -> None:
        if roll is not None:
            self.add_roll(roll)

            def next_show_cb():
                self.query_one("#-scroll-window", VerticalScroll).scroll_end(
                    animate=False
                )
                self.app.set_focus(self.query(Roll).last())

            self.next_show_cb = next_show_cb
