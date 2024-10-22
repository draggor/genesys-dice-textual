from dataclasses import dataclass, field
from enum import StrEnum
import itertools
import random
from typing import List

from pprint import pprint


class Symbol(StrEnum):
    TRIUMPH = 'TR'
    SUCCESS = 'S'
    ADVANTAGE = 'A'
    DESPAIR = 'D'
    FAILURE = 'F'
    THREAT = 'TH'
    BLANK = 'B'

symbol_display = {
    Symbol.TRIUMPH: '❂',
    Symbol.SUCCESS: '✷',
    Symbol.ADVANTAGE: '⮝',
    Symbol.DESPAIR: '⦻',
    Symbol.FAILURE: '⨯',
    Symbol.THREAT: '⎊',
    Symbol.BLANK: ' ',
}

class Dice(StrEnum):
    BOOST = 'B'
    SETBACK = 'S'
    ABILITY = 'A'
    DIFFICULTY = 'D'
    PROFICIENCY = 'P'
    CHALLENGE = 'C'
    PERCENTILE = '%'

type Face = int | Symbol | list[Symbol]

@dataclass
class Die:
    faces: List[Face] = field(default_factory=list)

    def __init__(self, faces: List[Face]):
        self.faces = faces

Boost = Die([
    Symbol.BLANK,
    Symbol.BLANK,
    Symbol.SUCCESS,
    [Symbol.SUCCESS, Symbol.ADVANTAGE],
    [Symbol.ADVANTAGE, Symbol.ADVANTAGE],
    Symbol.ADVANTAGE,
])

Setback = Die([
    Symbol.BLANK,
    Symbol.BLANK,
    Symbol.FAILURE,
    Symbol.FAILURE,
    Symbol.THREAT,
    Symbol.THREAT,
])

Ability = Die([
    Symbol.BLANK,
    Symbol.SUCCESS,
    Symbol.SUCCESS,
    [Symbol.SUCCESS, Symbol.SUCCESS],
    Symbol.ADVANTAGE,
    Symbol.ADVANTAGE,
    [Symbol.SUCCESS, Symbol.ADVANTAGE],
    [Symbol.ADVANTAGE, Symbol.ADVANTAGE],
])

Difficulty = Die([
    Symbol.BLANK,
    Symbol.FAILURE,
    [Symbol.FAILURE, Symbol.FAILURE],
    Symbol.THREAT,
    Symbol.THREAT,
    Symbol.THREAT,
    [Symbol.THREAT, Symbol.THREAT],
    [Symbol.FAILURE, Symbol.THREAT],
])

Proficiency = Die([
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
])

Challenge = Die([
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
])

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

def roll_die(die: Die) -> Face:
    return random.choice(die.faces)

def add_result(results, result):
    match result:
        case int():
            results['Percentile'].append(result)
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
        'Percentile': [],
    }

    for result in results:
        if type(result) is list:
            for item in result:
                add_result(reduced, item)
        else:
            add_result(reduced, result)

    #return reduced
    composed_str = ''
    for symbol in [Symbol.TRIUMPH, Symbol.SUCCESS, Symbol.ADVANTAGE, Symbol.DESPAIR, Symbol.FAILURE, Symbol.THREAT]:
        composed_str += reduced[symbol]*symbol_display[symbol]

    return composed_str


# TODO: make results its own class for better tracking and future rendering
def roll(dice_str: str) -> List[Face]:
    results = []

    for die_str in dice_str:
        die = dice_map[die_str]
        # TODO: roll should be a method on die
        # TODO: need to match result to die type for better display
        result = roll_die(die)
        results.append(result)

    reduced = reduce_results(results)
    pprint(results)

    return reduced

#pprint(roll('PAADDD%%'))

def table():
    rows = set()
    for f1 in Proficiency.faces:
        for f2 in Ability.faces:
            for f3 in Ability.faces:
                for f4 in Difficulty.faces:
                    for f5 in Difficulty.faces:
                        rows.add(reduce_results([f1,f2,f3,f4,f5]))

    return rows

def table(dice_str):
    dice = [dice_map[d].faces for d in dice_str]
    combinations = itertools.product(*dice)
    combo_list = list(combinations)
    total = len(combo_list)
    reduced = {}
    for combo in combo_list:
        r = reduce_results(list(combo))
        if r in reduced:
            reduced[r] += 1
        else:
            reduced[r] = 1

    for item in reduced:
        reduced[item] = round(reduced[item] / total * 100, 2)

    return reduced


t = table('PAACC')
pprint(len(t))
pprint(t)
