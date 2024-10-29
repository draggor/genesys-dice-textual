from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Placeholder

from dice import (
    roll,
    results_table,
    success_probability,
    dice_map,
    Dice,
    Die,
    symbol_display,
)


color_map = {
    Dice.BOOST: "cyan",
    Dice.SETBACK: "black",
    Dice.ABILITY: "ansi_green",
    Dice.DIFFICULTY: "darkorchid",
    Dice.PROFICIENCY: "gold",
    Dice.CHALLENGE: "darkred",
    Dice.PERCENTILE: "lightslategrey",
}


class Die(Button):
    def __init__(self, die: Die, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.die = die
        self.label = die.die_type
        self.styles.background = color_map[die.die_type]


class DiceMenu(Container):
    DEFAULT_CSS = """
    DiceMenu {
        height: 1fr;
        width: 1fr;
        layout: grid;
        grid-size: 7;
    }
    """

    def compose(self) -> ComposeResult:
        for die_type, die in dice_map.items():
            yield Die(die, id=die_type.name)


class Pending(Placeholder):
    DEFAULT_CSS = """
    Pending {
        height: 1fr;
        width: 1fr;
    }
    """


class Tray(Horizontal):
    def compose(self) -> ComposeResult:
        yield Pending(id="Pending")
        yield DiceMenu(id="DiceMenu")


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
