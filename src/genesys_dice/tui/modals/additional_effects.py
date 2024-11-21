from typing import List, Optional

from rich.console import Group
from rich.padding import Padding
from rich.panel import Panel
from rich.text import Text

from textual.app import ComposeResult
from textual.containers import Middle, Horizontal, Vertical, ItemGrid
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


class EffectOption(Static):

    def __init__(self, effect: AdditionalEffectOption, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.update(
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


class AdditionalEffectsModal(ModalScreen):
    DEFAULT_CSS = """
    AdditionalEffectsModal {
        align: center middle;

        #-effects-container {
            max-width: 80%;
            max-height: 90%;
            width: 100%;
            height: auto;
            layout: grid;
            grid-size: 2;
            grid-rows: auto;
            grid-columns: 1fr 2fr;

            Middle {
                width: 1fr;
                height: auto;

                SelectionList {
                    width: 100%;
                    height: auto;
                    border: solid white;
                }
            }
        }

        #-selected-container {
            width: 100%;
            height: auto;
        }

        #-effect-selected {
            width: 100%;
            height: auto;
        }

        #-effect-option {
            width: 100%;
            height: auto;
        }
    }
    """

    BINDINGS = [
        ("escape", "app.pop_screen()", "Cancel"),
    ]

    additional_effects: AdditionalEffects

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.additional_effects = data.load_from_file(
            "roll-builders.yaml", AdditionalEffects
        )[0]

    def compose(self) -> ComposeResult:
        options = []
        max_difficulty_len = self.additional_effects.max_difficulty_len()
        for option in self.additional_effects.options:
            symbols = get_dice_symbols(option.difficulty, pad=max_difficulty_len)
            options.append(Selection(symbols + " " + option.name, option))

        with ItemGrid(id="-effects-container"):
            with Middle():
                yield SelectionList[AdditionalEffectOption](*options)
            with Vertical(id="-selected-container"):
                yield Static(id="-effect-option")
                yield Static(id="-effect-selected")

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
                )
            )
        )

    def format_effect(self, effect):
        return Padding(
            Panel(
                effect.description,
                title=effect.name,
                title_align="left",
                subtitle=get_dice_symbols(effect.difficulty),
                subtitle_align="left",
            ),
        )

    def on_selection_list_selected_changed(self, event) -> None:
        selected_text = []
        for selected in event.control.selected:
            selected_text.append(self.format_effect(selected))
        selected_static = self.query_one("#-effect-selected", Static)
        selected_static.update(Group(*selected_text))
