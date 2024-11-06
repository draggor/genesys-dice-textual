from rich.table import Table

from genesys_dice.dice import dice_faces


def get_faces_table() -> Table:
    data = dice_faces()

    table = Table(title="Dice Faces")
    table.add_column(data[0][0], justify="right", style="cyan")

    for i in range(1, 13):
        table.add_column(data[0][i], justify="center", style="magenta")

    for row in data[1:]:
        table.add_row(*row)

    return table
