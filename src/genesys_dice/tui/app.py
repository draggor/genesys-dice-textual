from typing import Optional, cast

import pyperclip  # type: ignore

from rich.text import Text

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label, Placeholder, Static

from genesys_dice.dice import (
    Dice,
    DicePool,
    dice_display,
    Modifier,
    modifier_display,
    Result,
)

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

    def modify_dice(self, die_type: Dice, modifier: Optional[Modifier] = None) -> None:
        self.dice_pool.modify(die_type, modifier)
        self.mutate_reactive(Pending.dice_pool)

    def clear_dice(self) -> None:
        self.dice_pool = DicePool()


class Tray(Vertical):

    roll_result: reactive[Result] = reactive(Result)

    def compose(self) -> ComposeResult:
        with Horizontal(id="TrayUpper"):
            yield Pending(id="Pending", border_title="Pending Dice")
            yield DiceMenu(id="DiceMenu", border_title="Dice Menu")
        with Horizontal(id="TrayLower"):
            with Horizontal():
                # yield TitleLabel(id="RollString", border_title="Short Code")
                # yield TitleLabel(id="RollDetails", border_title="Details")
                # yield TitleLael(id="RollResult", border_title="Result")
                yield TitleButton(
                    label="",
                    id="RollString",
                    classes="copy",
                    border_title="Short Code",
                )
                yield TitleButton(
                    id="RollDetails", classes="copy", border_title="Details"
                )
                yield TitleButton(
                    id="RollResult", classes="copy", border_title="Result"
                )
            with Container(id="RollButtons"):
                yield Button("Roll!", id="Roll", variant="success")
                yield Button("Clear!", id="Clear", variant="error")

    def watch_roll_result(self, roll_result: Result) -> None:
        self.query_one("#RollResult", TitleButton).label = str(roll_result)
        formatted_details = Text(roll_result.details_str(), justify="left")
        self.query_one("#RollDetails", TitleButton).label = formatted_details

    @on(Button.Pressed, ".copy")
    def copy_roll_str(self, message: TitleButton.Pressed) -> None:
        pyperclip.copy(message.control.label)

    @on(Button.Pressed, ".tray")
    def modify_pending_dice(self, message: DieButton.Pressed) -> None:
        die_button = cast(DieButton, message.control)
        pending = self.query_one(Pending)
        pending.modify_dice(die_button.die_type, die_button.modifier)
        dice_roll_str = pending.dice_pool.roll_str()
        self.query_one("#RollString", TitleButton).label = dice_roll_str

    @on(Button.Pressed, ".pending")
    def remove_pending_dice(self, message: DieButton.Pressed) -> None:
        die_button = cast(DieButton, message.control)
        pending = self.query_one(Pending)
        pending.modify_dice(die_button.die_type, Modifier.REMOVE)
        dice_roll_str = pending.dice_pool.roll_str()
        self.query_one("#RollString", TitleButton).label = dice_roll_str

    @on(Button.Pressed, "#Roll")
    def roll_dice(self, message: Button.Pressed) -> None:
        self.roll_result = self.query_one(Pending).dice_pool.roll()

    @on(Button.Pressed, "#Clear")
    def clear_dice(self, message: Button.Pressed) -> None:
        self.roll_result = Result()
        self.query_one(Pending).clear_dice()
        self.query_one("#RollString", TitleButton).label = ""


class TrayScreen(Screen):
    CSS_PATH = "app.tcss"

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
