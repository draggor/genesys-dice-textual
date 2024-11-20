from typing import Optional

from rich.padding import Padding
from rich.panel import Panel

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import (
    SelectionList,
    Static,
)
from textual.widgets.selection_list import Selection

from genesys_dice import data
from genesys_dice.dice import AdditionalEffects, AdditionalEffectOption
from genesys_dice.tui.rich.dice_faces import get_dice_symbols


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

            #-effect-option {
                width: 2fr;
                height: auto;
            }
        }
    }
    """

    additional_effects: AdditionalEffects
    effect_display: reactive[Optional[AdditionalEffectOption]] = reactive(None)

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
            yield Static(id="-effect-option")

    def on_selection_list_selection_highlighted(self, event) -> None:
        details = self.query_one("#-effect-option", Static)
        effect = event.selection.value
        details.update(
            Padding(
                Panel(
                    effect.description,
                    title=effect.name,
                    title_align="left",
                    subtitle=get_dice_symbols(effect.difficulty),
                    subtitle_align="left",
                ),
                (0, 0, 1, 0),
            )
        )
