from collections.abc import Callable
import math
from typing import Optional, List

from rich.text import TextType

from textual import on, events
from textual.app import ComposeResult
from textual.containers import (
    Center,
    ItemGrid,
    Vertical,
    VerticalScroll,
)
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import (
    Static,
    TabPane,
)

from genesys_dice import data
from genesys_dice.dice import DicePool
from genesys_dice.tui.messages import (
    CopyCommandMessage,
    SaveRollMessage,
    SwitchTabMessage,
)
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

        #-center-dice-container {
            width: 100%;
            height: auto;
        }

        #-dice-container {
            layout: grid;
            grid-size: 6;
            grid-rows: auto;
            grid-columns: auto;
            grid-gutter: 0 1;
            width: auto;
            height: auto;
        }

        .-button-display {
            margin: 0 0;

            &:disabled {
                opacity: 1;
            }
        }

        #-roll-description {
            margin: 1 0 0 0;
        }
    }
    """

    BINDINGS = [
        ("enter", "send_roll_to_tray()", "Send roll to tray"),
        ("e", "edit_roll()", "Edit selected roll"),
        ("ctrl+o", "copy_command_text()", "Copy Command"),
    ]

    dice_pool: reactive[DicePool] = reactive(DicePool)

    def __init__(
        self,
        dice_pool: DicePool,
        *children: Widget,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            *children, name=name, id=id, classes=classes, disabled=disabled
        )
        self.dice_pool = dice_pool
        self.border_title: str = dice_pool.name

    def compose(self) -> ComposeResult:
        with Center(id="-center-dice-container"):
            with ItemGrid(id="-dice-container"):
                for die_type in self.dice_pool.get_dice():
                    yield DieButton(die_type, disabled=True, classes="-button-display")
        yield Static(self.dice_pool.description, id="-roll-description")

    def action_copy_command_text(self) -> None:
        self.post_message(CopyCommandMessage(self.dice_pool))

    def action_send_roll_to_tray(self) -> None:
        self.app.set_focus(None)
        self.post_message(SwitchTabMessage("tray-tab", self.dice_pool))

    def action_edit_roll(self) -> None:
        self.post_message(SaveRollMessage(self.dice_pool))

    def calculate_grid_columns(self) -> None:
        available_size = self.container_size.width - 3
        max_dice = math.floor(available_size / 6)
        dice_count = self.dice_pool.count()
        columns = dice_count if dice_count < max_dice else max_dice
        self.query_one(ItemGrid).styles.grid_size_columns = columns

    def on_show(self) -> None:
        self.calculate_grid_columns()

    def on_resize(self) -> None:
        self.calculate_grid_columns()

    @on(events.Enter)
    @on(events.Leave)
    def on_enter(self, event: events.Enter) -> None:
        event.stop()
        self.set_class(self.is_mouse_over, "-hover")

    @on(events.Click)
    def handle_click(self, event: events.Click) -> None:
        """
        A widget becomes focused on mouse_down right away.
        We use -activated class to check if we're ready
        to send the roll to the tray, aka, need to click twice.
        """
        event.stop()
        if self.is_mouse_over and self.has_class("-activated"):
            self.action_send_roll_to_tray()
        else:
            self.add_class("-activated")

    @on(events.Blur)
    def handle_unfocus(self) -> None:
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
    next_show_cb: Optional[Callable[[], None]] = None

    def __init__(
        self,
        title: TextType,
        *children: Widget,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            title, *children, name=name, id=id, classes=classes, disabled=disabled
        )

        self.saved_rolls = data.load_from_file("test-data.yaml", DicePool)

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="-scroll-window") as container:
            container.can_focus = False
            with ItemGrid(id="-item-grid", min_column_width=32):
                for roll in self.saved_rolls:
                    yield Roll(roll)

    def on_show(self, event: events.Show) -> None:
        if self.next_show_cb is not None:
            self.next_show_cb()
            self.next_show_cb = None

    def add_roll(self, roll: DicePool) -> None:
        if roll not in self.saved_rolls:
            self.saved_rolls.append(roll)
        self.mutate_reactive(SavedRolls.saved_rolls)

    def set_data(self, roll: Optional[DicePool] = None) -> None:
        if roll is not None:
            self.add_roll(roll)

            def next_show_cb() -> None:
                self.query_one("#-scroll-window", VerticalScroll).scroll_end(
                    animate=False
                )
                self.app.set_focus(self.query(Roll).last())

            self.next_show_cb = next_show_cb
