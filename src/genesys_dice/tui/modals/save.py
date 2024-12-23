from typing import Optional

from textual import on
from textual.app import ComposeResult
from textual.containers import Grid, Vertical
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, TextArea

from genesys_dice.dice import DicePool
from genesys_dice.tui.widgets import DieButton, LabelInput, LabelTextArea


class SaveModal(ModalScreen[Optional[DicePool]]):

    DEFAULT_CSS = """
    SaveModal {
        align: center middle;

        #-save-container {
            padding: 0 1;
            width: auto;
            max-width: 80%;
            height: auto;
            border: thick $background 80%;
            background: $surface;

            Button {
                width: 1fr;
                height: 3;
                margin: 1 1 0 1;
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

            LabelTextArea {
                width: 100%;
                height: 12;
                margin: 0;
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

                DieButton:disabled {
                    opacity: 1;
                }
            }
        }
    }
    """

    dice_pool: reactive[DicePool] = reactive(DicePool, recompose=True)

    def __init__(self, dice: DicePool) -> None:
        super().__init__()
        self.dice_pool = dice

    def compose(self) -> ComposeResult:
        with Vertical(id="-save-container"):
            yield Label("Save Dialog", id="-save-title")

            yield LabelInput(
                label_args=["Name of the roll"],
                label_kwargs={"classes": "inner"},
                input_kwargs={
                    "placeholder": "Name of the roll",
                    "classes": "inner",
                    "value": self.dice_pool.name,
                },
            )

            yield Label("Save these dice:", classes="info")

            with Grid(id="-save-dice-grid"):
                for die_type in self.dice_pool.get_dice():
                    yield DieButton(die_type, disabled=True)

            yield LabelTextArea(
                label_args=["Description"],
                label_kwargs={"classes": "inner"},
                text_area_kwargs={
                    "classes": "inner",
                    "text": self.dice_pool.description,
                },
            )

            yield Button("Save", variant="primary", id="-save-button")
            yield Button("Cancel", variant="error", id="-cancel-button")

    @on(Button.Pressed, "#-save-button")
    def save_modal(self, message: Button.Pressed) -> None:
        name = self.query_one(Input).value
        description = self.query_one(TextArea).text
        self.dice_pool.name = name
        self.dice_pool.description = description
        self.dismiss(self.dice_pool)

    @on(Button.Pressed, "#-cancel-button")
    def cancel_modal(self) -> None:
        self.dismiss()
