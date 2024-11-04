from typing import Optional, cast

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Placeholder

from dice import (
    Dice,
    DicePool,
    dice_display,

    Modifier,
    modifier_display,
)

from die_button import DieButton


class DiceMenu(Container):
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


class Pending(Container):

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


class Tray(Horizontal):
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Pending(id="Pending")
            with Horizontal(id="RollButtons"):
                yield Placeholder(id="RollString")
                yield Placeholder(id="RollResult")
        with Vertical():
            yield DiceMenu(id="DiceMenu")
            yield Placeholder(id="RollButtons")

    @on(Button.Pressed, ".tray")
    def modify_pending_dice(self, message: DieButton.Pressed) -> None:
        die_button = cast(DieButton, message.control)
        self.query_one(Pending).modify_dice(die_button.die_type, die_button.modifier)

    @on(Button.Pressed, ".pending")
    def remove_pending_dice(self, message: DieButton.Pressed) -> None:
        die_button = cast(DieButton, message.control)
        self.query_one(Pending).modify_dice(die_button.die_type, Modifier.REMOVE)


class TrayScreen(Screen):
    CSS_PATH = "tray_screen.tcss"

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
