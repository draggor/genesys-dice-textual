from typing import Optional

from rich.padding import Padding
from rich.panel import Panel
from rich.text import Text

from textual.app import ComposeResult
from textual.containers import Grid, Horizontal, Vertical, ItemGrid
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    Input,
    Label,
    TextArea,
    SelectionList,
    Placeholder,
    Static,
)
from textual.widgets.selection_list import Selection

from genesys_dice import data
from genesys_dice.dice import DicePool, AdditionalEffects, AdditionalEffectOption
from genesys_dice.tui.messages import SaveRollMessage
from genesys_dice.tui.widgets import DieButton, LabelInput, LabelTextArea


class EffectDisplay(Static):
    additional_effect: Optional[AdditionalEffectOption] = reactive(None)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def watch_additional_effect(self, effect) -> None:
        if effect is not None:
            self.update(
                Padding(
                    Panel(
                        effect.description,
                        title=effect.name,
                        title_align="left",
                        subtitle=effect.difficulty,
                        subtitle_align="left",
                    ),
                    (0, 0, 1, 0),
                )
            )


class AdditionalEffectsModal(ModalScreen):
    DEFAULT_CSS = """
    AdditionalEffectsModal {
        align: center middle;

        #-effects-container {
            max-width: 80%;
            max-height: 90%;
            width: 100%;
            height: auto;
            align: center middle;

            SelectionList {
                width: 1fr;
                height: auto;
                border: solid white;
            }

            EffectDisplay {
                width: 2fr;
                height: auto;
            }
        }
    }
    """

    additional_effects: AdditionalEffects

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.additional_effects = data.load_from_file(
            "roll-builders.yaml", AdditionalEffects
        )[0]

    def compose(self) -> ComposeResult:
        options = []
        for option in self.additional_effects.options:
            options.append(Selection(option.name, option))

        with Horizontal(id="-effects-container"):
            yield SelectionList[AdditionalEffectOption](*options)
            yield EffectDisplay(id="-effect-option")

    def on_selection_list_selection_highlighted(self, event) -> None:
        self.query_one(EffectDisplay).additional_effect = event.selection.value
