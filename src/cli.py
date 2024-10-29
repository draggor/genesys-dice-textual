import click
from rich.console import Console
from rich.pretty import pprint
from rich.table import Table

from dice import (
    roll,
    results_table,
    success_probability,
    dice_map,
    Dice,
    symbol_display,
)


@click.command()
@click.option("-t", is_flag=True, help="Print all rolls with probabilities")
@click.option("-s", is_flag=True, help="Print the success rate of a roll")
@click.option("-f", is_flag=True, help="Print the faces of the dice")
@click.argument("dice", required=False)
def main(t, s, f, dice):
    """
    A dice roller and probablity calculator for the Genesys RPG system

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
        success_rate = success_probability(dice)
        pprint(f"Success rate for {dice} is {success_rate}%")
    elif t:
        result, success_rate = results_table(dice)

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
    elif f:
        table = Table(title="Dice Faces")
        table.add_column("Die", justify="right", style="cyan")

        for i in range(1, 13):
            table.add_column(str(i), justify="center", style="magenta")

        for die_type, die in dice_map.items():
            if die_type is Dice.PERCENTILE:
                pass
            else:
                row = [die_type.name]
                for face in die.faces:
                    if type(face) is list:
                        row.append(" ".join([symbol_display[f] for f in face]))
                    else:
                        row.append(symbol_display[face])
                table.add_row(*row)

        console = Console()
        console.print(table)
    else:
        if dice is None:
            click.echo(click.get_current_context().get_help())
        else:
            result = roll(dice)

            click.echo(result)


if __name__ == "__main__":
    main()
