from rich.table import Table
from rich.text import Text

from genesys_dice.dice import dice_faces, Dice


def get_faces_table() -> Table:
    data = dice_faces()

    table = Table(title="Dice Faces")
    table.add_column(data[0][0], justify="right", style="cyan")

    for i in range(1, 13):
        table.add_column(data[0][i], justify="center", style="magenta")

    for row in data[1:]:
        table.add_row(*row)

    return table


def get_die_symbol(short_code):
    die_type = Dice.from_short_code(short_code)
    symbol, color = die_type.symbol

    return Text(symbol, style=color)


def get_dice_symbols(short_codes, pad=0):
    symbol_str = Text()
    for short_code in short_codes:
        if Dice.has_short_code(short_code):
            symbol_str += get_die_symbol(short_code)
        else:
            symbol_str += Text(short_code)

    to_pad = pad - len(symbol_str)

    return Text(to_pad * " ") + symbol_str
