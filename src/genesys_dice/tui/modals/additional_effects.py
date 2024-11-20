from rich.padding import Padding
from rich.panel import Panel
from rich.text import Text

from textual.app import ComposeResult
from textual.containers import Grid, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, TextArea, OptionList
from textual.widgets.option_list import Option, Separator

from genesys_dice import data
from genesys_dice.dice import DicePool, AdditionalEffects, AdditionalEffectOption
from genesys_dice.tui.messages import SaveRollMessage
from genesys_dice.tui.widgets import DieButton, LabelInput, LabelTextArea


class AdditionalEffectOption(Option):
    addional_effect: AdditionalEffectOption

    def __init__(self, option: AdditionalEffectOption) -> None:
        self.addional_effect = option
        panel = Padding(
            Panel(
                option.description,
                title=option.name,
                title_align="left",
                subtitle=option.difficulty,
                subtitle_align="left",
            ),
            (0, 0, 1, 0),
        )
        super().__init__(panel)


class AdditionalEffectsModal(ModalScreen):
    DEFAULT_CSS = """
    AdditionalEffectsModal {
        align: center middle;

        #-effects-container {
            max-width: 80%;
            max-height: 90%;
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
            options.append(AdditionalEffectOption(option))

        with Vertical(id="-effects-container"):
            yield OptionList(*options)
