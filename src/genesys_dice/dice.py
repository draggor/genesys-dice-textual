from collections import Counter
from dataclasses import dataclass, field
from enum import StrEnum
import itertools
import random
from typing import Any, Dict, List, Optional, Tuple, Self, cast


# TODO: Formatting for foundry, see https://github.com/StarWarsFoundryVTT/StarWarsFFG/wiki/FAQ#how-do-i-manually-roll-dice


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
    Symbol.BLANK: "□",
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
for die_type, code in dice_display.items():
    dice_short_codes[code] = die_type

type Face = int | Symbol | list[Symbol]
type DieResult = tuple[Dice, Face]


@dataclass
class Die:
    die_type: Dice
    faces: List[Face] = field(default_factory=list)
    upgrade: Optional[Dice] = None
    downgrade: Optional[Dice] = None

    def roll(self) -> DieResult:
        return self.die_type, random.choice(self.faces)


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
    upgrade=Dice.ABILITY,
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
    upgrade=Dice.DIFFICULTY,
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
    downgrade=Dice.BOOST,
    upgrade=Dice.PROFICIENCY,
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
    downgrade=Dice.SETBACK,
    upgrade=Dice.CHALLENGE,
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
    downgrade=Dice.ABILITY,
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
    downgrade=Dice.DIFFICULTY,
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

    @staticmethod
    def default_totals() -> Dict[Any, Any]:
        return {
            Symbol.TRIUMPH: 0,
            Symbol.SUCCESS: 0,
            Symbol.ADVANTAGE: 0,
            Symbol.DESPAIR: 0,
            Symbol.FAILURE: 0,
            Symbol.THREAT: 0,
            "Percentile": [],
        }

    results: List[Face] = field(default_factory=list)

    details: Dict[Dice, List[Face]] = field(default_factory=dict, init=False)
    totals: Dict[Any, Any] = field(default_factory=default_totals, init=False)
    _success: Optional[bool] = field(default=None, init=False)

    def __post_init__(self) -> None:
        if len(self.results) > 0:
            self.reduce()

    @property
    def success(self) -> Optional[bool]:
        return self._success

    def reduce(self) -> Self:
        for face in self.results:
            if type(face) is list:
                for symbol in face:
                    self.add_symbol(symbol)
            else:
                self.add_symbol(face)

        if self.totals[Symbol.SUCCESS] > 0:
            self._success = True
        elif self.totals[Symbol.FAILURE] > 0:
            self._success = False
        else:
            self._success = None

        return self

    def add_symbol(self, result: Face) -> None:
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

    def add(self, result: DieResult) -> None:
        die_type, face = result

        if die_type in self.details:
            self.details[die_type].append(face)
        else:
            self.details[die_type] = [face]

        self.results.append(face)

    def details_str(self) -> str:
        lines = []

        for die_type, faces in self.details.items():
            composed_str = f"{dice_display[die_type]}: "
            str_faces = []
            for face in faces:
                if type(face) is list:
                    str_faces.append(" ".join([symbol_display[s] for s in face]))
                elif type(face) is int:
                    str_faces.append(str(face))
                else:
                    symbol_key = cast(Symbol, face)
                    str_faces.append(symbol_display[symbol_key])
            composed_str += " | ".join(str_faces)
            lines.append(composed_str)

        return "\n".join(lines)

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


@dataclass()
class DicePool:
    @staticmethod
    def default_dice() -> Dict[Dice, int]:
        d = {}

        for die_type in dice_display.keys():
            d[die_type] = 0

        return d

    dice_counts: Dict[Dice, int] = field(default_factory=default_dice, init=False)
    dice: str = ""

    def __post_init__(self) -> None:
        for die_type in get_dice_from_str(self.dice):
            self.dice_counts[die_type] += 1

    def modify(self, die_type: Dice, modifier: Optional[Modifier] = None) -> Self:
        die = dice_map[die_type]

        match modifier:
            case Modifier.ADD:
                self.dice_counts[die_type] += 1
            case Modifier.UPGRADE:
                if die.upgrade and self.dice_counts[die_type] > 0:
                    self.dice_counts[die_type] -= 1
                    self.dice_counts[die.upgrade] += 1
                else:
                    self.dice_counts[die_type] += 1
            case Modifier.REMOVE:
                if self.dice_counts[die_type] > 0:
                    self.dice_counts[die_type] -= 1
            case Modifier.DOWNGRADE:
                if self.dice_counts[die_type] > 0:
                    if die.downgrade:
                        self.dice_counts[die_type] -= 1
                        self.dice_counts[die.downgrade] += 1
                    else:
                        self.dice_counts[die_type] -= 1
            case _:
                pass

        self.dice = self.roll_str()

        return self

    def roll(self) -> Result:
        roll_result = Result()

        for die_type in self.get_dice():
            die = dice_map[die_type]
            die_result: DieResult = die.roll()
            roll_result.add(die_result)

        return roll_result.reduce()

    def get_dice(self) -> List[Dice]:
        dice = []

        for die_type, count in self.dice_counts.items():
            for _ in range(1, count + 1):
                dice.append(die_type)

        return dice

    def get_dice_faces(self) -> List[List[Face]]:
        faces = []

        for die_type in self.get_dice():
            die = dice_map[die_type]
            faces.append(die.faces)

        return faces

    def success_probability(self) -> float:
        dice_faces = self.get_dice_faces()
        product = list(itertools.product(*dice_faces))
        total = len(product)
        success_count = 0

        for result in product:
            if is_success(list(result)):
                success_count += 1

        return round(success_count / total * 100, 2)

    def results_table(self) -> Tuple[Dict[str, float], float]:
        dice_faces = self.get_dice_faces()
        product = list(itertools.product(*dice_faces))
        total = len(product)
        reduced: Dict[str, float] = {}
        success_count = 0
        for combo in product:
            r = str(Result(list(combo)).reduce())

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

    def roll_str(self) -> str:
        composed_str = ""

        for die_type, count in self.dice_counts.items():
            composed_str += dice_display[die_type] * count

        return composed_str

    def is_empty(self) -> bool:
        return sum(self.dice_counts.values()) == 0

    def __str__(self) -> str:
        return self.dice


def get_dice_from_str(dice_str: str) -> List[Dice]:
    dice = []
    for die_str in dice_str.strip().upper():
        if die_str in dice_short_codes:
            dice.append(dice_short_codes[die_str])
        else:
            raise Exception(f"{die_str} is not a valid short code")

    return dice


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


def dice_faces() -> List[List[str]]:
    table = [["Die"]]

    for i in range(1, 13):
        table[0].append(str(i))

    for die_type, die in dice_map.items():
        if die_type is Dice.PERCENTILE:
            pass
        else:
            row = [die_type.name]
            for face in die.faces:
                if type(face) is list:
                    row.append(" ".join([symbol_display[f] for f in face]))
                else:
                    symbol = cast(Symbol, face)
                    row.append(symbol_display[symbol])
            table.append(row)

    return table
