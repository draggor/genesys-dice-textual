from textual import on
from textual.app import ComposeResult
from textual.containers import Grid, Horizontal, Vertical
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, TabbedContent

from genesys_dice.data import SavedRoll
from genesys_dice.dice import DicePool
from genesys_dice.tui.widgets import DieButton, LabelInput


class SaveModal(ModalScreen):

    DEFAULT_CSS = """
    SaveModal {
        align: center middle;

        #-save-container {
            padding: 0 1;
            width: 60;
            height: auto;
            border: thick $background 80%;
            background: $surface;

            #-save-footer {
                dock: bottom;
                width: 100%;
                height: 3;

                Button {
                    width: 1fr;
                    height: 3;
                    margin: 0 1;
                }
            }

            #-save-title {
                dock: top;
                height: 3;
                width: 1fr;
                background: $primary-background;
                content-align: center middle;
            }

            LabelInput {
                width: 100%;
                margin: 1 0;
                height: auto;
            }

            .info {
                margin: 0 1;
            }

            #-save-dice-grid {
                layout: grid;
                grid-size: 8;
                grid-gutter: 0;
                grid-rows: 5;
                grid-columns: 7;
                height: auto;
            }
        }
    }
    """

    dice_pool: reactive[DicePool] = reactive(DicePool, recompose=True)

    def compose(self) -> ComposeResult:
        with Vertical(id="-save-container"):
            yield Label("Save Dialog", id="-save-title")

            yield LabelInput(
                label_args=["Name of the roll"],
                label_kwargs={"classes": "inner"},
                input_kwargs={"placeholder": "Name of the roll", "classes": "inner"},
            )

            yield Label("Save these dice:", classes="info")

            with Grid(id="-save-dice-grid"):
                for die_type in self.dice_pool.get_dice():
                    yield DieButton(die_type, disabled=True)

            with Horizontal(id="-save-footer"):
                yield Button("Save", variant="primary", id="-save-button")
                yield Button("Cancel", variant="error", id="-cancel-button")

    @on(Button.Pressed, "#-save-button")
    def save_modal(self, message: Button.Pressed) -> None:
        name = self.query_one(Input).value
        dice_str = self.dice_pool.roll_str()
        self.dismiss(SavedRoll(name, dice_str))

    @on(Button.Pressed, "#-cancel-button")
    def cancel_modal(self) -> None:
        self.dismiss()
