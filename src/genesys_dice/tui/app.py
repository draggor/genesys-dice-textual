from typing import Iterable, Optional


from textual.app import App, ComposeResult, SystemCommand
from textual.screen import Screen
from textual.widgets import (
    Button,
    Header,
    Footer,
    TabbedContent,
    TabPane,
)

from genesys_dice.tui.modals import DiceFacesModal
from genesys_dice.tui.tabs import Tray, SavedRolls


class AppScreen(Screen):
    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield Header(id="Header")

        with TabbedContent(initial="tray-tab"):
            with TabPane("Dice Tray", id="tray-tab"):
                yield Tray(id="Tray")
            with TabPane("Saved Rolls", id="savedrolls-tab"):
                yield SavedRolls(id="SavedRolls")

        yield Footer(id="Footer")


class DiceApp(App):
    BINDINGS = [
        ("f", "show_dice_faces_modal()", "Show Dice Faces"),
    ]

    starting_dice: Optional[str] = None

    def __init__(self, dice_str: Optional[str] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.starting_dice = dice_str

    async def on_mount(self) -> None:
        await self.push_screen(AppScreen())
        if self.starting_dice is not None:
            self.query_one(Tray).set_dice(self.starting_dice)
            self.query_one("#Save", Button).press()

    def action_show_dice_faces_modal(self) -> None:
        self.push_screen(DiceFacesModal())

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        yield from super().get_system_commands(screen)
        yield SystemCommand(
            "Show Dice Faces",
            "Pop up a modal window with the dice faces table.",
            self.action_show_dice_faces_modal,
        )


if __name__ == "__main__":
    app = DiceApp()
    app.run()
