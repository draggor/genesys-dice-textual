from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Button, Label, TabbedContent

from genesys_dice.dice import DicePool


class SaveModal(ModalScreen):

    DEFAULT_CSS = """
    SaveModal {
        align: center middle;

        #save-dialog {
            grid-size: 2;
            grid-gutter: 1 2;
            grid-rows: 1fr 3;
            padding: 0 1;
            width: 60;
            height: 11;
            border: thick $background 80%;
            background: $surface;

            Button {
                width: 100%;
            }
        }
    }
    """

    dice_pool: reactive[DicePool] = reactive(DicePool, recompose=True)

    def __init__(self, dice_pool: DicePool, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dice_pool = dice_pool

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Save these dice:"),
            Label(self.dice_pool.roll_str()),
            Button("Save", variant="primary", id="save"),
            Button("Cancel", variant="error", id="cancel"),
            id="save-dialog",
        )

    @on(Button.Pressed, "#save")
    def save_modal(self, message: Button.Pressed) -> None:
        self.dismiss("bees")

    @on(Button.Pressed, "#cancel")
    def cancel_modal(self) -> None:
        self.dismiss()
