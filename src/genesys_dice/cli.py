from typing import cast

import click
from rich.console import Console
from rich.pretty import pprint
from rich.table import Table

from genesys_dice.dice import (
    dice_display,
    dice_faces,
    DicePool,
    symbol_display,
    Symbol,
)

from genesys_dice.tui.rich import get_faces_table
from genesys_dice.tui.app import DiceApp


def command_success(dice: str) -> None:
    success_rate = DicePool(dice).success_probability()
    pprint(f"Success rate for {dice} is {success_rate}%")


def command_table(dice: str) -> None:
    result, success_rate = DicePool(dice).results_table()

    count = len(result)
    table = Table(title=f"Results for dice {dice} ({count})", show_footer=True)
    table.add_column(
        "Result", justify="right", style="cyan", no_wrap=True, footer="Success Rate"
    )
    table.add_column("%", justify="right", style="magenta")

    for rolls, probability in result.items():
        table.add_row(rolls, str(probability))

    table.columns[1].footer = str(success_rate) + "%"

    console = Console()
    console.print(table)


def command_faces() -> None:
    table = get_faces_table()
    console = Console()
    console.print(table)


def command_roll(dice: str, details: bool):
    result = DicePool(dice).roll()
    if details:
        for die_type, faces in result.details.items():
            composed_str = f"{dice_display[die_type]}: "
            str_faces = []
            for face in faces:
                if type(face) is list:
                    str_faces.append(" ".join([symbol_display[s] for s in face]))
                else:
                    symbol_key = cast(Symbol, face)
                    str_faces.append(symbol_display[symbol_key])
            composed_str += " | ".join(str_faces)
            click.echo(composed_str)
    click.echo(str(result))


@click.command()
@click.option("-d", is_flag=True, help="Print the details of the roll")
@click.option("-t", is_flag=True, help="Print all rolls with probabilities")
@click.option("-s", is_flag=True, help="Print the success rate of a roll")
@click.option("-f", is_flag=True, help="Print the faces of the dice")
@click.option("-u", is_flag=True, help="Run the TUI with initial dice")
@click.argument("dice", required=False)
def main(d, t, s, f, u, dice):
    """
    \b
    A dice roller and probablity calculator for the Genesys RPG system.
    If run without any arguments, it loads the interactive TUI.

    The dice short codes are:

    \b
    BOOST = B
    SETBACK = S
    ABILITY = A
    DIFFICULTY = D
    PROFICIENCY = P
    CHALLENGE = C
    PERCENTILE = T

    1 Proficiency (yellow) 2 Ability (green) against 2 Difficulty (purple) is: PAADD
    """

    if s:
        command_success(dice)
    elif t:
        command_table(dice)
    elif f:
        command_faces()
    else:
        if dice is None:
            app = DiceApp()
            app.run()
        elif u:
            app = DiceApp(dice)
            app.run()
        else:
            command_roll(dice, d)


if __name__ == "__main__":
    main()
