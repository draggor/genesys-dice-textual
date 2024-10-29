from textual.app import ComposeResult
from textual.css._error_tools import friendly_list
from textual.widgets import Button

from typing_extensions import Literal, Self

from dice import Die, Dice, dice_display


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
    $boost: cyan;
    $boost-darken-1: $boost;
    $boost-darken-2: $boost;
    $boost-darken-3: $boost;
    $boost-lighten-2: $boost;
    $boost-lighten-3: $boost;
    $setback: black;
    $setback-darken-1: $setback;
    $setback-darken-2: $setback;
    $setback-darken-3: $setback;
    $setback-lighten-2: $setback;
    $setback-lighten-3: $setback;
    $ability: ansi_green;
    $ability-darken-1: $ability;
    $ability-darken-2: $ability;
    $ability-darken-3: $ability;
    $ability-lighten-2: $ability;
    $ability-lighten-3: $ability;
    $difficulty: darkorchid;
    $difficulty-darken-1: $difficulty;
    $difficulty-darken-2: $difficulty;
    $difficulty-darken-3: $difficulty;
    $difficulty-lighten-2: $difficulty;
    $difficulty-lighten-3: $difficulty;
    $proficiency: gold;
    $proficiency-darken-1: $proficiency;
    $proficiency-darken-2: $proficiency;
    $proficiency-darken-3: $proficiency;
    $proficiency-lighten-2: $proficiency;
    $proficiency-lighten-3: $proficiency;
    $challenge: darkred;
    $challenge-darken-1: $challenge;
    $challenge-darken-2: $challenge;
    $challenge-darken-3: $challenge;
    $challenge-lighten-2: $challenge;
    $challenge-lighten-3: $challenge;
    $percentile: lightslategrey;
    $percentile-darken-1: $percentile;
    $percentile-darken-2: $percentile;
    $percentile-darken-3: $percentile;
    $percentile-lighten-2: $percentile;
    $percentile-lighten-3: $percentile;

    DieButton {
        width: auto;
        min-width: 16;
        height: auto;
        background: $panel;
        color: $text;
        border: none;
        border-top: tall $panel-lighten-2;
        border-bottom: tall $panel-darken-3;
        text-align: center;
        content-align: center middle;
        text-style: bold;


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
            background: $boost;
            color: $text;
            border-top: tall $boost-lighten-3;
            border-bottom: tall $boost-darken-3;

            &:hover {
                background: $boost-darken-2;
                color: $text;
                border-top: tall $boost;
            }

            &.-active {
                background: $boost;
                border-bottom: tall $boost-lighten-3;
                border-top: tall $boost-darken-3;
            }
        }

        &.-setback {
            background: $setback;
            color: $text;
            border-top: tall $setback-lighten-2;
            border-bottom: tall $setback-darken-3;

            &:hover {
                background: $setback-darken-2;
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
                border-top: tall $ability;
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
                color: $text;
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
                background: $proficiency-darken-1;
                color: $text;
                border-top: tall $proficiency;
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
                color: $text;
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
                color: $text;
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

    # variant = reactive(Dice.ABILITY, init=False)
    """The variant name for the button."""

    def __init__(self, die: Die, *args, **kwargs):
        super().__init__(variant=die.die_type, *args, **kwargs)
        self.die = die
        self.label = dice_display[die.die_type]
        # self.variant = die.die_type
        # self.styles.background = color_map[die.die_type]

    def validate_variant(self, variant: str) -> str:
        if variant not in _VALID_DIE_VARIANTS:
            raise InvalidDieVariant(
                f"Valid die variants are {friendly_list(_VALID_DIE_VARIANTS)}"
            )
        return variant
