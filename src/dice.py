from collections import Counter
from dataclasses import dataclass, field
from enum import StrEnum
import itertools
import random
from typing import Any, Dict, List, Tuple

from rich.pretty import pprint


class Symbol(StrEnum):
    TRIUMPH = "triumph"
    SUCCESS = "success"
    ADVANTAGE = "advantage"
    DESPAIR = "despair"
    FAILURE = "failure"
    THREAT = "threat"
    BLANK = "blank"


symbol_display = {
    Symbol.TRIUMPH: "❂",
    Symbol.SUCCESS: "✷",
    Symbol.ADVANTAGE: "▲",
    Symbol.DESPAIR: "⦻",
    Symbol.FAILURE: "⨯",
    Symbol.THREAT: "⎊",
    Symbol.BLANK: " ",
}


class Modifier(StrEnum):
    ADD = "add"
    UPGRADE = "upgrade"
    REMOVE = "remove"
    DOWNGRADE = "downgrade"


modifier_display = {
    Modifier.ADD: "+",
    Modifier.UPGRADE: "↑",
    Modifier.REMOVE: "-",
    Modifier.DOWNGRADE: "↓",
}


class Dice(StrEnum):
    BOOST = "boost"
    SETBACK = "setback"
    ABILITY = "ability"
    DIFFICULTY = "difficulty"
    PROFICIENCY = "proficiency"
    CHALLENGE = "challenge"
    PERCENTILE = "percentile"


dice_display = {
    Dice.PROFICIENCY: "P",
    Dice.ABILITY: "A",
    Dice.BOOST: "B",
    Dice.CHALLENGE: "C",
    Dice.DIFFICULTY: "D",
    Dice.SETBACK: "S",
    Dice.PERCENTILE: "%",
}

dice_short_codes = {}
for die, code in dice_display.items():
    dice_short_codes[code] = die

type Face = int | Symbol | list[Symbol]


@dataclass
class Die:
    faces: List[Face] = field(default_factory=list)

    def __init__(self, die_type: Dice, faces: List[Face]):
        self.faces = faces
        self.die_type = die_type

    def roll(self) -> Face:
        return random.choice(self.faces)


Boost = Die(
    Dice.BOOST,
    [
        Symbol.BLANK,
        Symbol.BLANK,
        Symbol.SUCCESS,
        [Symbol.SUCCESS, Symbol.ADVANTAGE],
        [Symbol.ADVANTAGE, Symbol.ADVANTAGE],
        Symbol.ADVANTAGE,
    ],
)

Setback = Die(
    Dice.SETBACK,
    [
        Symbol.BLANK,
        Symbol.BLANK,
        Symbol.FAILURE,
        Symbol.FAILURE,
        Symbol.THREAT,
        Symbol.THREAT,
    ],
)

Ability = Die(
    Dice.ABILITY,
    [
        Symbol.BLANK,
        Symbol.SUCCESS,
        Symbol.SUCCESS,
        [Symbol.SUCCESS, Symbol.SUCCESS],
        Symbol.ADVANTAGE,
        Symbol.ADVANTAGE,
        [Symbol.SUCCESS, Symbol.ADVANTAGE],
        [Symbol.ADVANTAGE, Symbol.ADVANTAGE],
    ],
)

Difficulty = Die(
    Dice.DIFFICULTY,
    [
        Symbol.BLANK,
        Symbol.FAILURE,
        [Symbol.FAILURE, Symbol.FAILURE],
        Symbol.THREAT,
        Symbol.THREAT,
        Symbol.THREAT,
        [Symbol.THREAT, Symbol.THREAT],
        [Symbol.FAILURE, Symbol.THREAT],
    ],
)

Proficiency = Die(
    Dice.PROFICIENCY,
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
    ],
)

Challenge = Die(
    Dice.CHALLENGE,
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
    ],
)

Percentile = Die(Dice.PERCENTILE, list(range(1, 101)))

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


def get_dice_from_str(dice_str: str) -> List[Die]:
    dice = []
    for die in dice_str.strip().upper():
        if die in dice_short_codes:
            dice.append(dice_map[dice_short_codes[die]])
        else:
            raise Exception(f"{die} is not a valid short code")

    return dice


def get_dice_faces(dice: List[Die]) -> List[List[Face]]:
    dice_faces = [die.faces for die in dice if die is not Dice.PERCENTILE]
    return dice_faces


def roll(dice: List[Die]) -> str:
    results = []

    for die in dice:
        result = die.roll()
        results.append(result)

    reduced = Result(results)
    str_results = str(reduced)
    return str_results


def count_symbols(roll_result: List[Face]) -> Dict[Symbol, int]:
    flat: List[Symbol] = []
    for face in roll_result:
        if type(face) is list:
            flat.extend(face)
        elif type(face) is Symbol:
            flat.append(face)
        else:
            raise Exception(f"{face} is a buggy face?")
    return Counter(flat)


def is_success(roll_result: List[Face]) -> bool:
    counts = count_symbols(roll_result)
    return (counts[Symbol.SUCCESS] + counts[Symbol.TRIUMPH]) > (
        counts[Symbol.FAILURE] + counts[Symbol.DESPAIR]
    )


def success_probability(dice: List[Die]) -> float:
    dice_faces = get_dice_faces(dice)
    product = list(itertools.product(*dice_faces))
    total = len(product)
    success_count = 0

    for result in product:
        if is_success(list(result)):
            success_count += 1

    return round(success_count / total * 100, 2)


def results_table(dice: List[Die]) -> Tuple[Dict[str, float], float]:
    dice_faces = get_dice_faces(dice)
    product = list(itertools.product(*dice_faces))
    total = len(product)
    reduced: Dict[str, float] = {}
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
