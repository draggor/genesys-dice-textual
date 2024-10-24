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


def results_table(dice_str: str) -> Dict[Any, Any]:
    dice_faces = [dice_map[die_str].faces for die_str in dice_str]
    product = list(itertools.product(*dice_faces))
    total = len(product)
    reduced = {}
    for combo in product:
        r = str(Result(list(combo)))
        if r in reduced:
            reduced[r] += 1
        else:
            reduced[r] = 1

    for item in reduced:
        reduced[item] = round(reduced[item] / total * 100, 2)

    return reduced


@click.command()
@click.option("-t", is_flag=True, help="Print all rolls with probabilities")
@click.argument("dice")
def main(t, dice):
    if t:
        result = results_table(dice)

        count = len(result)
        table = Table(title=f"Results for dice {dice} ({count})")
        table.add_column("Result", justify="right", style="cyan", no_wrap=True)
        table.add_column("%", justify="right", style="magenta")

        for rolls, probability in result.items():
            table.add_row(rolls, str(probability))

        console = Console()
        console.print(table)
    else:
        result = roll(dice)

        click.echo(result)


if __name__ == "__main__":
    main()
