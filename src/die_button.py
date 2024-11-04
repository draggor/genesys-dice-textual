from textual.css._error_tools import friendly_list
from textual.widgets import Button

from typing_extensions import Literal, Optional

from dice import Dice, dice_display, Modifier, modifier_display


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
        width: 5;
        min-width: 2;
        max-width: 5;
        height: 3;
        min-height: 1;
        max-height: 3;
        background: $panel;
        color: $text;
        border: none;
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
            background: $panel-darken-2;
            color: $text;
        }
        &.-active {
            background: $panel;
            tint: $background 30%;
        }

        &.-boost {
            background: $boost;
            color: $text;

            &:hover {
                background: $boost-darken-2;
                color: $text;
            }

            &.-active {
                background: $boost;
            }
        }

        &.-setback {
            background: $setback;
            color: $text;

            &:hover {
                background: $setback-darken-2;
                color: $text;
            }

            &.-active {
                background: $setback;
            }
        }

        &.-ability{
            background: $ability;
            color: $background;

            &:hover {
                background: $ability-darken-2;
                color: $text;
            }

            &.-active {
                background: $ability;
            }
        }

        &.-difficulty {
            background: $difficulty;
            color: $text;

            &:hover {
                background: $difficulty-darken-1;
                color: $text;
            }

            &.-active {
                background: $difficulty;
            }
        }

        &.-proficiency {
            background: $proficiency;
            color: $text;

            &:hover {
                background: $proficiency-darken-1;
                color: $text;
            }

            &.-active {
                background: $proficiency;
            }
        }

        &.-challenge {
            background: $challenge;
            color: $text;

            &:hover {
                background: $challenge-darken-1;
                color: $text;
            }

            &.-active {
                background: $challenge;
            }
        }

        &.-percentile {
            background: $percentile;
            color: $text;

            &:hover {
                background: $percentile-darken-1;
                color: $text;
            }

            &.-active {
                background: $percentile;
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
