from dataclasses import field
from typing import Any, Dict, List, Optional, Tuple, cast

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, HorizontalGroup, VerticalGroup
from textual.message import Message
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label, Placeholder, Static

from dice import (
    results_table,
    success_probability,
    dice_map,
    Dice,
    DicePool,
    Die,
    dice_display,
    symbol_display,
    Modifier,
    modifier_display,
)

from die_button import DieButton


class DiceMenu(Container):
    DEFAULT_CSS = """
    DiceMenu {
        height: 28;
        width: 50%;
    }
    """

    def compose(self) -> ComposeResult:
        for die_type in dice_display.keys():
            row = []
            die = dice_map[die_type]

            for mod in modifier_display.keys():
                if die_type is Dice.PERCENTILE and mod in [
                    Modifier.UPGRADE,
                    Modifier.DOWNGRADE,
                ]:
                    pass
                else:
                    row.append(
                        DieButton(
                            die,
                            modifier=mod,
                            id=f"{die_type.name}-{mod.name}",
                            classes="tray modifier",
                        )
                    )
            yield Horizontal(*row)


class Pending(Container):
    DEFAULT_CSS = """
    Pending {
        height: 100%;
        width: 50%;

        Container {
            height: 28;
        }

        #dice_string {
            dock: bottom;
            height: 1;
            content-align: center middle;
        }
    }
    """

    dice_pool: reactive[DicePool] = reactive(DicePool, recompose=True)

    def compose(self) -> ComposeResult:
        yield Static(str(self.dice_pool), id="dice_string")

        css_id: int = 0

        with Container():
            for die_type, count in self.dice_pool.dice.items():
                die = dice_map[die_type]
                row = []
                for _ in range(1, count + 1):
                    css_id += 1
                    row.append(
                        DieButton(die, id=f"{die_type.name}{css_id}", classes="pending")
                    )

                yield Horizontal(*row)

    def modify_dice(self, die: Die, modifier: Optional[Modifier] = None) -> None:
        self.dice_pool.modify(die, modifier)
        self.mutate_reactive(Pending.dice_pool)


class Tray(Horizontal):
    def compose(self) -> ComposeResult:
        yield Pending(id="Pending")
        yield DiceMenu(id="DiceMenu")

    @on(Button.Pressed, ".tray")
    def modify_pending_dice(self, message: DieButton.Pressed) -> None:
        die_button = cast(DieButton, message.control)
        self.query_one(Pending).modify_dice(die_button.die, die_button.modifier)


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
