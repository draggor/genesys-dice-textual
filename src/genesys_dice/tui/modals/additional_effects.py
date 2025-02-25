from typing import List, Optional

from rich.console import Group
from rich.padding import Padding
from rich.panel import Panel
from rich.text import Text

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Middle, Horizontal, Vertical, ItemGrid
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import (
    SelectionList,
    Static,
)
from textual.widgets.selection_list import Selection

from genesys_dice import data
from genesys_dice.dice import (
    AdditionalEffects,
    AdditionalEffectOption,
    Dice,
    DicePool,
    Modifier,
)
from genesys_dice.tui.rich.dice_faces import get_dice_symbols


class AdditionalEffectsModal(ModalScreen[None]):
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

            Vertical {
                width: 1fr;
                height: auto;

                SelectionList {
                    width: 100%;
                    height: auto;
                    border: solid white;
                }
            }
        }

        #-effect-header {
            width: 1fr;
            text-align: center;
            text-style: bold;
            border: solid white;
        }

        #-current-dice {
            width: 2fr;
            text-align: center;
            text-style: bold;
            border: solid white;
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
        ("escape,m", "dismiss()", "Close"),
        Binding("j", "focused.cursor_down", "Down", show=False),
        Binding("k", "focused.cursor_up", "Up", show=False),
    ]

    additional_effects: AdditionalEffects
    dice_pool: DicePool

    def __init__(self, dice_pool: DicePool, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dice_pool = dice_pool
        self.additional_effects = data.load_from_file(
            "roll-builders.yaml", AdditionalEffects
        )[0]

    def compose(self) -> ComposeResult:
        options = []
        max_difficulty_len = self.additional_effects.max_difficulty_len()
        for option in self.additional_effects.options:
            symbols = get_dice_symbols(option.difficulty, pad=max_difficulty_len)
            selected = option in self.dice_pool.additional_effects
            options.append(
                Selection(symbols + " " + option.name, option, initial_state=selected)
            )

        with ItemGrid(id="-effects-container"):
            yield Static(
                "Modify Roll",
                id="-effect-header",
            )
            yield Static(
                Text("Current Dice: ") + get_dice_symbols(self.dice_pool.roll_str()),
                id="-current-dice",
            )
            with Vertical():
                yield SelectionList[AdditionalEffectOption](*options)
            with Vertical(id="-selected-container"):
                yield Static(id="-effect-option")
                yield Static(id="-effect-selected")

    def on_selection_list_selection_highlighted(
        self, event: SelectionList.SelectionHighlighted[AdditionalEffectOption]
    ) -> None:
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

    def format_effect(self, effect: AdditionalEffectOption) -> Padding:
        return Padding(
            Panel(
                effect.description,
                title=effect.name,
                title_align="left",
                subtitle=get_dice_symbols(effect.difficulty),
                subtitle_align="left",
            ),
        )

    def update_current_dice(self) -> None:
        self.query_one("#-current-dice", Static).update(
            Text("Current Dice: ") + get_dice_symbols(self.dice_pool.roll_str())
        )

    def on_selection_list_selection_toggled(
        self, event: SelectionList.SelectionToggled[AdditionalEffectOption]
    ) -> None:
        effect = event.selection.value
        selected = effect in event.selection_list.selected

        if selected:
            self.dice_pool.add_additional_effect(effect)
        else:
            self.dice_pool.remove_additional_effect(effect)

        self.update_current_dice()

    def on_selection_list_selected_changed(
        self, event: SelectionList.SelectedChanged[AdditionalEffectOption]
    ) -> None:
        # selected_text = []
        # for selected in event.control.selected:
        #    selected_text.append(self.format_effect(selected))
        # selected_static = self.query_one("#-effect-selected", Static)
        # selected_static.update(Group(*selected_text))
        pass
