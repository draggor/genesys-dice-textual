import click
from rich.console import Console
from rich.pretty import pprint
from rich.table import Table

from dice import (
    results_table,
    success_probability,
    dice_display,
    dice_map,
    dice_faces,
    Dice,
    DicePool,
    symbol_display,
    get_dice_from_str,
)


@click.command()
@click.option("-d", is_flag=True, help="Print the details of the roll")
@click.option("-t", is_flag=True, help="Print all rolls with probabilities")
@click.option("-s", is_flag=True, help="Print the success rate of a roll")
@click.option("-f", is_flag=True, help="Print the faces of the dice")
@click.argument("dice", required=False)
def main(d, t, s, f, dice):
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
        success_rate = DicePool(dice).success_probability()
        pprint(f"Success rate for {dice} is {success_rate}%")
    elif t:
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
    elif f:
        data = dice_faces()

        table = Table(title="Dice Faces")
        table.add_column(data[0][0], justify="right", style="cyan")

        for i in range(1, 13):
            table.add_column(data[0][i], justify="center", style="magenta")

        for row in data[1:]:
            table.add_row(*row)

        console = Console()
        console.print(table)
    else:
        if dice is None:
            click.echo(click.get_current_context().get_help())
        else:
            result = DicePool(dice).roll()
            if d:
                for die_type, faces in result.details.items():
                    composed_str = f"{dice_display[die_type]}: "
                    str_faces = []
                    for face in faces:
                        if type(face) is list:
                            str_faces.append(
                                " ".join([symbol_display[s] for s in face])
                            )
                        else:
                            str_faces.append(symbol_display[face])
                    composed_str += " | ".join(str_faces)
                    click.echo(composed_str)
            click.echo(str(result))


if __name__ == "__main__":
    main()
