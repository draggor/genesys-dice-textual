from collections import Counter
from dataclasses import dataclass, field
from enum import StrEnum
import itertools
import random
from typing import Any, Dict, List

import click
from rich.console import Console
from rich.pretty import pprint
from rich.table import Table


class Symbol(StrEnum):
    TRIUMPH = "TR"
    SUCCESS = "S"
    ADVANTAGE = "A"
    DESPAIR = "D"
    FAILURE = "F"
    THREAT = "TH"
    BLANK = "B"


symbol_display = {
    Symbol.TRIUMPH: "❂",
    Symbol.SUCCESS: "✷",
    Symbol.ADVANTAGE: "▲",
    Symbol.DESPAIR: "⦻",
    Symbol.FAILURE: "⨯",
    Symbol.THREAT: "⎊",
    Symbol.BLANK: " ",
}


class Dice(StrEnum):
    BOOST = "B"
    SETBACK = "S"
    ABILITY = "A"
    DIFFICULTY = "D"
    PROFICIENCY = "P"
    CHALLENGE = "C"
    PERCENTILE = "%"


type Face = int | Symbol | list[Symbol]


@dataclass
class Die:
    faces: List[Face] = field(default_factory=list)

    def __init__(self, faces: List[Face]):
        self.faces = faces

    def roll(self) -> Face:
        return random.choice(self.faces)


Boost = Die(
    [
        Symbol.BLANK,
        Symbol.BLANK,
        Symbol.SUCCESS,
        [Symbol.SUCCESS, Symbol.ADVANTAGE],
        [Symbol.ADVANTAGE, Symbol.ADVANTAGE],
        Symbol.ADVANTAGE,
    ]
)

Setback = Die(
    [
        Symbol.BLANK,
        Symbol.BLANK,
        Symbol.FAILURE,
        Symbol.FAILURE,
        Symbol.THREAT,
        Symbol.THREAT,
    ]
)

Ability = Die(
    [
        Symbol.BLANK,
        Symbol.SUCCESS,
        Symbol.SUCCESS,
        [Symbol.SUCCESS, Symbol.SUCCESS],
        Symbol.ADVANTAGE,
        Symbol.ADVANTAGE,
        [Symbol.SUCCESS, Symbol.ADVANTAGE],
        [Symbol.ADVANTAGE, Symbol.ADVANTAGE],
    ]
)

Difficulty = Die(
    [
        Symbol.BLANK,
        Symbol.FAILURE,
        [Symbol.FAILURE, Symbol.FAILURE],
        Symbol.THREAT,
        Symbol.THREAT,
        Symbol.THREAT,
        [Symbol.THREAT, Symbol.THREAT],
        [Symbol.FAILURE, Symbol.THREAT],
    ]
)

Proficiency = Die(
    [
        Symbol.BLANK,
        Symbol.SUCCESS,
        Symbol.SUCCESS,
        [Symbol.SUCCESS, Symbol.SUCCESS],
        [Symbol.SUCCESS, Symbol.SUCCESS],
        Symbol.ADVANTAGE,
        [Symbol.SUCCESS, Symbol.ADVANTAGE],
        [Symbol.SUCCESS, Symbol.ADVANTAGE],
        [Symbol.SUCCESS, Symbol.ADVANTAGE],
        [Symbol.ADVANTAGE, Symbol.ADVANTAGE],
        [Symbol.ADVANTAGE, Symbol.ADVANTAGE],
        Symbol.TRIUMPH,
    ]
)

Challenge = Die(
    [
        Symbol.BLANK,
        Symbol.FAILURE,
        Symbol.FAILURE,
        [Symbol.FAILURE, Symbol.FAILURE],
        [Symbol.FAILURE, Symbol.FAILURE],
        Symbol.THREAT,
        Symbol.THREAT,
        [Symbol.FAILURE, Symbol.THREAT],
        [Symbol.FAILURE, Symbol.THREAT],
        [Symbol.THREAT, Symbol.THREAT],
        [Symbol.THREAT, Symbol.THREAT],
        Symbol.DESPAIR,
    ]
)

Percentile = Die(list(range(1, 101)))

dice_map = {
    Dice.BOOST: Boost,
    Dice.SETBACK: Setback,
    Dice.ABILITY: Ability,
    Dice.DIFFICULTY: Difficulty,
    Dice.PROFICIENCY: Proficiency,
    Dice.CHALLENGE: Challenge,
    Dice.PERCENTILE: Percentile,
}

cancel_map = {
    Symbol.THREAT: Symbol.ADVANTAGE,
    Symbol.ADVANTAGE: Symbol.THREAT,
    Symbol.FAILURE: Symbol.SUCCESS,
    Symbol.SUCCESS: Symbol.FAILURE,
    Symbol.DESPAIR: Symbol.SUCCESS,
    Symbol.TRIUMPH: Symbol.FAILURE,
}


@dataclass
class Result:
    totals: Dict[Any, Any]

    results: List[Face] = field(default_factory=list)

    def __init__(self, results: List[Face]) -> None:
        self.totals = {
            Symbol.TRIUMPH: 0,
            Symbol.SUCCESS: 0,
            Symbol.ADVANTAGE: 0,
            Symbol.DESPAIR: 0,
            Symbol.FAILURE: 0,
            Symbol.THREAT: 0,
            "Percentile": [],
        }
        self.results = results
        self.reduce(results)

    def reduce(self, results: List[Face]) -> None:
        for result in results:
            if type(result) is list:
                for item in result:
                    self.add(item)
            else:
                self.add(result)

    def add(self, result: Face) -> None:
        match result:
            case int():
                self.totals["Percentile"].append(result)
            case Symbol.BLANK:
                pass
            case Symbol():
                opposite = cancel_map[result]

                if result is Symbol.TRIUMPH or result is Symbol.DESPAIR:
                    result_add = cancel_map[opposite]
                    self.totals[result] += 1
                else:
                    result_add = result

                if self.totals[opposite] == 0:
                    self.totals[result_add] += 1
                else:
                    self.totals[opposite] -= 1

    def __str__(self) -> str:
        composed_str = ""
        for symbol in [
            Symbol.TRIUMPH,
            Symbol.SUCCESS,
            Symbol.ADVANTAGE,
            Symbol.DESPAIR,
            Symbol.FAILURE,
            Symbol.THREAT,
        ]:
            composed_str += self.totals[symbol] * symbol_display[symbol]

        composed_str = " ".join(composed_str)
        composed_str += " " + " ".join(map(str, self.totals["Percentile"]))

        return composed_str


def roll(dice_str: str) -> str:
    results = []

    for die_str in dice_str:
        die = dice_map[die_str]
        # TODO: need to match result to die type for better display
        result = die.roll()
        results.append(result)

    reduced = Result(results)
    str_results = str(reduced)
    return str_results


def count_symbols(roll_result) -> Dict[Any, Any]:
    flat = []
    for face in roll_result:
        if type(face) is list:
            flat.extend(face)
        else:
            flat.append(face)
    return Counter(flat)


def is_success(roll_result) -> bool:
    counts = count_symbols(roll_result)
    return (counts[Symbol.SUCCESS] + counts[Symbol.TRIUMPH]) > (
        counts[Symbol.FAILURE] + counts[Symbol.DESPAIR]
    )


def success_probability(dice_str: str) -> float:
    stripped_dice_str = dice_str.strip("%")
    dice_faces = [dice_map[die_str].faces for die_str in stripped_dice_str]
    product = list(itertools.product(*dice_faces))
    total = len(product)
    success_count = 0

    for result in product:
        if is_success(result):
            success_count += 1

    return round(success_count / total * 100, 2)


def results_table(dice_str: str) -> Dict[Any, Any]:
    stripped_dice_str = dice_str.strip("%")
    dice_faces = [dice_map[die_str].faces for die_str in stripped_dice_str]
    product = list(itertools.product(*dice_faces))
    total = len(product)
    reduced = {}
    success_count = 0
    for combo in product:
        r = str(Result(list(combo)))

        if symbol_display[Symbol.SUCCESS] in r:
            success_count += 1

        if r in reduced:
            reduced[r] += 1
        else:
            reduced[r] = 1

    for item in reduced:
        reduced[item] = round(reduced[item] / total * 100, 2)

    success_rate = round(success_count / total * 100, 2)

    return reduced, success_rate


@click.command()
@click.option("-t", is_flag=True, help="Print all rolls with probabilities")
@click.option("-s", is_flag=True, help="Print the success rate of a roll")
@click.argument("dice")
def main(t, s, dice):
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
    PERCENTILE = %

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
    else:
        result = roll(dice)

        click.echo(result)


if __name__ == "__main__":
    main()
