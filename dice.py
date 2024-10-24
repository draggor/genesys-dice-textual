from dataclasses import dataclass, field
from enum import StrEnum
import itertools
import random
from typing import List

from pprint import pprint


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


@dataclass
class Result:
    totals = {
        Symbol.TRIUMPH: 0,
        Symbol.SUCCESS: 0,
        Symbol.ADVANTAGE: 0,
        Symbol.DESPAIR: 0,
        Symbol.FAILURE: 0,
        Symbol.THREAT: 0,
        "Percentile": [],
    }

cancel_map = {
    Symbol.THREAT: Symbol.ADVANTAGE,
    Symbol.ADVANTAGE: Symbol.THREAT,
    Symbol.FAILURE: Symbol.SUCCESS,
    Symbol.SUCCESS: Symbol.FAILURE,
    Symbol.DESPAIR: Symbol.SUCCESS,
    Symbol.TRIUMPH: Symbol.FAILURE
}

def test_cancel(results, result):
    match result:
        case int():
            results['Percentile'].append(result)
        case Symbol():
            opposite = cancel_map[result]

            if result is Symbol.TRIUMPH or result is Symbol.DESPAIR:
                result_add = cancel_map[opposite]
                results[result] += 1
            else:
                result_add = result

            if results[opposite] == 0:
                results[result_add] += 1
            else:
                results[opposite] -= 1




def add_result(results, result):
    match result:
        case int():
            results["Percentile"].append(result)
        case Symbol():
            match result:
                case Symbol.ADVANTAGE:
                    if results[Symbol.THREAT] == 0:
                        results[Symbol.ADVANTAGE] += 1
                    else:
                        results[Symbol.THREAT] -= 1
                case Symbol.THREAT:
                    if results[Symbol.ADVANTAGE] == 0:
                        results[Symbol.THREAT] += 1
                    else:
                        results[Symbol.ADVANTAGE] -= 1
                case Symbol.SUCCESS:
                    if results[Symbol.FAILURE] == 0:
                        results[Symbol.SUCCESS] += 1
                    else:
                        results[Symbol.FAILURE] -= 1
                case Symbol.FAILURE:
                    if results[Symbol.SUCCESS] == 0:
                        results[Symbol.FAILURE] += 1
                    else:
                        results[Symbol.SUCCESS] -= 1
                case Symbol.TRIUMPH:
                    results[Symbol.TRIUMPH] += 1
                    if results[Symbol.FAILURE] == 0:
                        results[Symbol.SUCCESS] += 1
                    else:
                        results[Symbol.FAILURE] -= 1
                case Symbol.DESPAIR:
                    results[Symbol.DESPAIR] += 1
                    if results[Symbol.SUCCESS] == 0:
                        results[Symbol.FAILURE] += 1
                    else:
                        results[Symbol.SUCCESS] -= 1

    return results


def reduce_results(results: List[Face]):
    reduced = {
        Symbol.TRIUMPH: 0,
        Symbol.SUCCESS: 0,
        Symbol.ADVANTAGE: 0,
        Symbol.DESPAIR: 0,
        Symbol.FAILURE: 0,
        Symbol.THREAT: 0,
        "Percentile": [],
    }

    for result in results:
        if type(result) is list:
            for item in result:
                add_result(reduced, item)
        else:
            add_result(reduced, result)

    # return reduced
    composed_str = ""
    for symbol in [
        Symbol.TRIUMPH,
        Symbol.SUCCESS,
        Symbol.ADVANTAGE,
        Symbol.DESPAIR,
        Symbol.FAILURE,
        Symbol.THREAT,
    ]:
        composed_str += reduced[symbol] * symbol_display[symbol]

    return composed_str


# TODO: make results its own class for better tracking and future rendering
def roll(dice_str: str) -> List[Face]:
    results = []

    for die_str in dice_str:
        die = dice_map[die_str]
        # TODO: roll should be a method on die
        # TODO: need to match result to die type for better display
        result = die.roll()
        results.append(result)

    reduced = reduce_results(results)
    pprint(results)

    return ' '.join(reduced)


pprint(roll('PAADDD%%'))


def table(dice_str):
    dice_faces = [dice_map[die_str].faces for die_str in dice_str]
    product = list(itertools.product(*dice_faces))
    total = len(product)
    reduced = {}
    for combo in product:
        r = reduce_results(list(combo))
        r = " ".join(r)
        if r in reduced:
            reduced[r] += 1
        else:
            reduced[r] = 1

    for item in reduced:
        reduced[item] = round(reduced[item] / total * 100, 2)

    return reduced


#t = table("PAADD")
#pprint(len(t))
#pprint(t)
