from textual.css._error_tools import friendly_list
from textual.widgets import Button

from typing_extensions import Literal, Optional

from genesys_dice.dice import Dice, dice_display, Modifier, modifier_display


# Currently not used, but here's a reference
# color_map = {
#     Dice.BOOST: "cyan",
#     Dice.SETBACK: "black",
#     Dice.ABILITY: "ansi_green",
#     Dice.DIFFICULTY: "darkorchid",
#     Dice.PROFICIENCY: "gold",
#     Dice.CHALLENGE: "darkred",
#     Dice.PERCENTILE: "lightslategrey",
# }

DieVariant = Literal[
    Dice.BOOST,
    Dice.SETBACK,
    Dice.ABILITY,
    Dice.DIFFICULTY,
    Dice.PROFICIENCY,
    Dice.CHALLENGE,
    Dice.PERCENTILE,
]

_VALID_DIE_VARIANTS = {
    Dice.BOOST,
    Dice.SETBACK,
    Dice.ABILITY,
    Dice.DIFFICULTY,
    Dice.PROFICIENCY,
    Dice.CHALLENGE,
    Dice.PERCENTILE,
}


class InvalidDieVariant(Exception):
    """Exception raised if an invalid button variant is used."""


class DieButton(Button):
    DEFAULT_CSS = """
    $hover-light: floralwhite;
    $hover-dark:  #241f31;
    $bst: cyan;
    $bst-darken-1: #00D5D5;
    $bst-darken-2: #00AAAA;
    $bst-darken-3: #008080;
    $bst-lighten-2: #80FFFF;
    $bst-lighten-3: #AAFFFF;
    $setback: black;
    $setback-darken-1: $setback;
    $setback-darken-2: $setback;
    $setback-darken-3: $setback;
    $setback-lighten-1: #151515;
    $setback-lighten-2: #2B2B2B;
    $setback-lighten-3: #404040;
    $ability: #7CFC00;
    $ability-darken-1: #67D200;
    $ability-darken-2: #53A800;
    $ability-darken-3: #3E7E00;
    $ability-lighten-2: #A8FD55;
    $ability-lighten-3: #BEFE80;
    $difficulty: darkorchid;
    $difficulty-darken-1: #802AAA;
    $difficulty-darken-2: #662188;
    $difficulty-darken-3: #4D1966;
    $difficulty-lighten-2: #BB76DD;
    $difficulty-lighten-3: #CC99E6;
    $proficiency: gold;
    $proficiency-darken-1: #D5B300;
    $proficiency-darken-2: #AA8F00;
    $proficiency-darken-3: #806C00;
    $proficiency-lighten-2: #FFE455;
    $proficiency-lighten-3: #FFEB80;
    $challenge: darkred;
    $challenge-darken-1: #740000;
    $challenge-darken-2: #5D0000;
    $challenge-darken-3: #460000;
    $challenge-lighten-2: #B25555;
    $challenge-lighten-3: #C58080;
    $percentile: lightslategrey;
    $percentile-darken-1: #637180;
    $percentile-darken-2: #4F5B66;
    $percentile-darken-3: #3C444D;
    $percentile-lighten-2: #A4B0BB;
    $percentile-lighten-3: #BBC4CC;

    DieButton {
        width: 5;
        min-width: 2;
        max-width: 5;
        height: 3;
        min-height: 1;
        max-height: 3;
        background: $panel;
        color: $text;
        border: none;
        border-top: tall $panel-lighten-2;
        border-bottom: tall $panel-darken-3;
        text-align: center;
        content-align: center middle;
        text-style: bold;
        margin: 1;

        &.modifier {
            width: 6;
            min-width: 2;
            max-width: 6;
        }

        &:focus {
            text-style: bold reverse;
        }
        &:hover {
            border-top: tall $panel;
            background: $panel-darken-2;
            color: $text;
        }
        &.-active {
            background: $panel;
            border-bottom: tall $panel-lighten-2;
            border-top: tall $panel-darken-2;
            tint: $background 30%;
        }

        &.-boost {
            background: $bst;
            color: $text;
            border-top: tall $bst-lighten-3;
            border-bottom: tall $bst-darken-3;

            &:hover {
                background: $bst-darken-2;
                color: $text;
                border-top: tall $bst-darken-1;
            }

            &.-active {
                background: $bst;
                border-bottom: tall $bst-lighten-3;
                border-top: tall $bst-darken-3;
            }
        }

        &.-setback {
            background: $setback;
            color: $text;
            border-top: tall $setback-lighten-3;
            border-bottom: tall $setback-lighten-2;

            &:hover {
                background: $setback-lighten-1;
                color: $text;
                border-top: tall $setback;
            }

            &.-active {
                background: $setback;
                border-bottom: tall $setback-lighten-2;
                border-top: tall $setback-darken-2;
            }
        }

        &.-ability{
            background: $ability;
            color: $text;
            border-top: tall $ability-lighten-2;
            border-bottom: tall $ability-darken-3;

            &:hover {
                background: $ability-darken-2;
                color: $text;
                border-top: tall $ability-darken-1;
            }

            &.-active {
                background: $ability;
                border-bottom: tall $ability-lighten-2;
                border-top: tall $ability-darken-2;
            }
        }

        &.-difficulty {
            background: $difficulty;
            color: $text;
            border-top: tall $difficulty-lighten-2;
            border-bottom: tall $difficulty-darken-3;

            &:hover {
                background: $difficulty-darken-1;
                color: $hover-dark;
                border-top: tall $difficulty;
            }

            &.-active {
                background: $difficulty;
                border-bottom: tall $difficulty-lighten-2;
                border-top: tall $difficulty-darken-2;
            }
        }

        &.-proficiency {
            background: $proficiency;
            color: $text;
            border-top: tall $proficiency-lighten-2;
            border-bottom: tall $proficiency-darken-3;

            &:hover {
                background: $proficiency-darken-2;
                color: $text;
                border-top: tall $proficiency-darken-1;
            }

            &.-active {
                background: $proficiency;
                border-bottom: tall $proficiency-lighten-2;
                border-top: tall $proficiency-darken-2;
            }
        }

        &.-challenge {
            background: $challenge;
            color: $text;
            border-top: tall $challenge-lighten-2;
            border-bottom: tall $challenge-darken-3;

            &:hover {
                background: $challenge-darken-1;
                color: $hover-dark;
                border-top: tall $challenge;
            }

            &.-active {
                background: $challenge;
                border-bottom: tall $challenge-lighten-2;
                border-top: tall $challenge-darken-2;
            }
        }

        &.-percentile {
            background: $percentile;
            color: $text;
            border-top: tall $percentile-lighten-2;
            border-bottom: tall $percentile-darken-3;

            &:hover {
                background: $percentile-darken-1;
                color: $hover-light;
                border-top: tall $percentile;
            }

            &.-active {
                background: $percentile;
                border-bottom: tall $percentile-lighten-2;
                border-top: tall $percentile-darken-2;
            }
        }

    }
    """

    def __init__(
        self, die_type: Dice, modifier: Optional[Modifier] = None, *args, **kwargs
    ):
        super().__init__(variant=die_type, *args, **kwargs)  # type: ignore
        self.die_type = die_type
        self.modifier = modifier
        self.label = dice_display[die_type]
        if modifier is not None:
            self.label += modifier_display[modifier]

    def validate_variant(self, variant: str) -> str:
        if variant not in _VALID_DIE_VARIANTS:
            raise InvalidDieVariant(
                f"Valid die variants are {friendly_list(_VALID_DIE_VARIANTS)}"
            )
        return variant
