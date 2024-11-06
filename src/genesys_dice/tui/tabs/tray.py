from typing import Optional, cast

import pyperclip  # type: ignore

from rich.text import Text

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import (
    Button,
    Header,
    Footer,
    Label,
    TabbedContent,
)

from genesys_dice.dice import (
    Dice,
    DicePool,
    dice_display,
    Modifier,
    modifier_display,
    Result,
)
from genesys_dice.tui.modals import SaveModal
from genesys_dice.tui.modals.callbacks import switch_tab
from genesys_dice.tui.widgets import (
    DieButton,
    TitleButton,
    TitleContainer,
    TitleHorizontal,
    TitleLabel,
)


class DiceMenu(TitleContainer):

    def compose(self) -> ComposeResult:
        for die_type in dice_display.keys():
            row = []

            for mod in modifier_display.keys():
                if die_type is Dice.PERCENTILE and mod in [
                    Modifier.UPGRADE,
                    Modifier.DOWNGRADE,
                ]:
                    pass
                else:
                    row.append(
                        DieButton(
                            die_type,
                            modifier=mod,
                            id=f"{die_type.name}-{mod.name}",
                            classes="tray modifier",
                        )
                    )
            yield Horizontal(*row)


class Pending(TitleContainer):

    dice_pool: reactive[DicePool] = reactive(DicePool, recompose=True)

    def compose(self) -> ComposeResult:
        css_id: int = 0

        for die_type, count in self.dice_pool.dice.items():
            row = []
            for _ in range(1, count + 1):
                css_id += 1
                row.append(
                    DieButton(
                        die_type, id=f"{die_type.name}{css_id}", classes="pending"
                    )
                )

            yield Horizontal(*row)


class Tray(Vertical):

    dice_pool: reactive[DicePool] = reactive(DicePool, always_update=True)
    roll_result: reactive[Result] = reactive(Result)

    def compose(self) -> ComposeResult:
        with Horizontal(id="TrayUpper"):
            yield Pending(id="Pending", border_title="Pending Dice").data_bind(
                Tray.dice_pool
            )
            yield DiceMenu(id="DiceMenu", border_title="Dice Menu")
        with Horizontal(id="TrayLower"):
            with Horizontal():
                yield TitleButton(
                    label="",
                    id="RollString",
                    classes="copy",
                    border_title="Short Code",
                )
                yield TitleButton(
                    label="", id="RollDetails", classes="copy", border_title="Details"
                )
                yield TitleButton(
                    label="", id="RollResult", classes="copy", border_title="Result"
                )
            with Container(id="RollButtons"):
                yield Button("Roll!", id="Roll", variant="success")
                yield Button("Clear!", id="Clear", variant="error")
                yield Button("Save!", id="Save", variant="primary")

    def watch_dice_pool(self) -> None:
        dice_roll_str = self.dice_pool.roll_str()
        self.query_one("#RollString", TitleButton).label = dice_roll_str

    def watch_roll_result(self, roll_result: Result) -> None:
        self.query_one("#RollResult", TitleButton).label = str(roll_result)
        formatted_details = Text(roll_result.details_str(), justify="left")
        self.query_one("#RollDetails", TitleButton).label = formatted_details

    def set_dice(self, dice_str: Optional[str] = None) -> None:
        self.dice_pool = DicePool(dice_str)

    @on(Button.Pressed, ".copy")
    def copy_roll_str(self, message: TitleButton.Pressed) -> None:
        text = message.control.label
        if text is not None and len(text) > 0:
            pyperclip.copy(message.control.label)

    @on(Button.Pressed, ".tray")
    def modify_pending_dice(self, message: DieButton.Pressed) -> None:
        die_button = cast(DieButton, message.control)
        self.dice_pool.modify(die_button.die_type, die_button.modifier)
        self.mutate_reactive(Tray.dice_pool)

    @on(Button.Pressed, ".pending")
    def remove_pending_dice(self, message: DieButton.Pressed) -> None:
        die_button = cast(DieButton, message.control)
        self.dice_pool.modify(die_button.die_type, Modifier.REMOVE)
        self.mutate_reactive(Tray.dice_pool)

    @on(Button.Pressed, "#Roll")
    def roll_dice(self, message: Button.Pressed) -> None:
        self.roll_result = self.dice_pool.roll()

    @on(Button.Pressed, "#Clear")
    def clear_dice(self, message: Button.Pressed) -> None:
        self.roll_result = Result()
        self.dice_pool = DicePool()

    @on(Button.Pressed, "#Save")
    def save_dice(self, message: Button.Pressed) -> None:
        if not self.dice_pool.is_empty():
            callback = switch_tab("template-tab", self.app)
            self.app.push_screen(SaveModal().data_bind(Tray.dice_pool), callback)
