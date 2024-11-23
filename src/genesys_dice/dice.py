from collections import Counter
from dataclasses import asdict, dataclass, field, is_dataclass
from enum import StrEnum, Enum
import itertools
import random
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Self,
    cast,
)


class Symbol(StrEnum):
    TRIUMPH = "triumph"
    SUCCESS = "success"
    ADVANTAGE = "advantage"
    DESPAIR = "despair"
    FAILURE = "failure"
    THREAT = "threat"
    BLANK = "blank"

    @property
    def unicode(self) -> "SymbolDisplay":
        return SymbolDisplay[self.name]

    @property
    def opposite(self) -> "Symbol":
        return Symbol[CancelMap[self.name].name]


class SymbolDisplay(StrEnum):
    TRIUMPH = "❂"
    SUCCESS = "✷"
    ADVANTAGE = "▲"
    DESPAIR = "⦻"
    FAILURE = "⨯"
    THREAT = "⎊"
    BLANK = "□"


class CancelMap(StrEnum):
    THREAT = Symbol.ADVANTAGE
    ADVANTAGE = Symbol.THREAT
    FAILURE = Symbol.SUCCESS
    SUCCESS = Symbol.FAILURE
    DESPAIR = Symbol.SUCCESS
    TRIUMPH = Symbol.FAILURE
    BLANK = Symbol.BLANK


class Modifier(StrEnum):
    ADD = "add"
    UPGRADE = "upgrade"
    REMOVE = "remove"
    DOWNGRADE = "downgrade"

    @property
    def unicode(self) -> "ModifierDisplay":
        return ModifierDisplay[self.name]

    @property
    def opposite(self) -> "Modifier":
        return Modifier[ModifierOpposite[self.name].name]


class ModifierDisplay(StrEnum):
    ADD = "+"
    UPGRADE = "↑"
    REMOVE = "-"
    DOWNGRADE = "↓"


class ModifierOpposite(StrEnum):
    ADD = Modifier.REMOVE
    REMOVE = Modifier.ADD
    UPGRADE = Modifier.DOWNGRADE
    DOWNGRADE = Modifier.UPGRADE


dice_symbol_display: Dict["Dice", Tuple[str, str]] = {}
dice_map: Dict["Dice", "Die"] = {}


class FoundryCode(StrEnum):
    PROFICIENCY = "dp"
    ABILITY = "da"
    BOOST = "db"
    CHALLENGE = "dc"
    DIFFICULTY = "di"
    SETBACK = "ds"
    PERCENTILE = ""


class DiceShortCode(StrEnum):
    PROFICIENCY = "P"
    ABILITY = "A"
    BOOST = "B"
    CHALLENGE = "C"
    DIFFICULTY = "D"
    SETBACK = "S"
    PERCENTILE = "%"

    @staticmethod
    def exists(short_code: str) -> bool:
        try:
            DiceShortCode(short_code)
            return True
        except:
            return False

    @property
    def die(self) -> "Dice":
        return Dice[self.name]


class Dice(StrEnum):
    PROFICIENCY = "proficiency"
    ABILITY = "ability"
    BOOST = "boost"
    CHALLENGE = "challenge"
    DIFFICULTY = "difficulty"
    SETBACK = "setback"
    PERCENTILE = "percentile"

    @property
    def short_code(self) -> DiceShortCode:
        return DiceShortCode[self.name]

    @property
    def symbol(self) -> Tuple["DiceSymbolDisplay", "DiceSymbolColor"]:
        return DiceSymbolDisplay[self.name], DiceSymbolColor[self.name]

    @property
    def foundry(self) -> FoundryCode:
        return FoundryCode[self.name]

    @property
    def die(self) -> "Die":
        return dice_map[self]

    @property
    def faces(self) -> List["Face"]:
        return dice_map[self].faces

    @property
    def upgrade(self) -> Optional["Dice"]:
        return dice_map[self].upgrade

    @property
    def downgrade(self) -> Optional["Dice"]:
        return dice_map[self].downgrade

    def roll(self) -> "DieResult":
        return dice_map[self].roll()

    @staticmethod
    def has_short_code(short_code: str) -> bool:
        try:
            DiceShortCode(short_code)
            return True
        except:
            return False

    @staticmethod
    def from_short_code(short_code: str) -> "Dice":
        return Dice[DiceShortCode(short_code).name]


class DiceSymbolDisplay(StrEnum):
    PROFICIENCY = "⬣"
    ABILITY = "⯁"
    BOOST = "◼"
    CHALLENGE = "⬣"
    DIFFICULTY = "⯁"
    SETBACK = "◼"
    PERCENTILE = "◼"


class DiceSymbolColor(StrEnum):
    PROFICIENCY = "#fff200"
    ABILITY = "#41ad49"
    BOOST = "#72cddc"
    CHALLENGE = "#B25555"
    DIFFICULTY = "#BB76DD"
    SETBACK = "#000000"
    PERCENTILE = "#A4B0BB"


Face = int | Symbol | list[Symbol]
DieResult = tuple[Dice, Face]


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

dice_map[Dice.BOOST] = Boost
dice_map[Dice.SETBACK] = Setback
dice_map[Dice.ABILITY] = Ability
dice_map[Dice.DIFFICULTY] = Difficulty
dice_map[Dice.PROFICIENCY] = Proficiency
dice_map[Dice.CHALLENGE] = Challenge
dice_map[Dice.PERCENTILE] = Percentile


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
                opposite = result.opposite

                if result is Symbol.TRIUMPH or result is Symbol.DESPAIR:
                    result_add = opposite.opposite
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
            composed_str = f"{die_type.short_code}: "
            str_faces = []
            for face in faces:
                if type(face) is list:
                    str_faces.append(" ".join([s.unicode for s in face]))
                elif type(face) is int:
                    str_faces.append(str(face))
                else:
                    symbol = cast(Symbol, face)
                    str_faces.append(symbol.unicode)
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
            composed_str += self.totals[symbol] * symbol.unicode

        composed_str = " ".join(composed_str)
        composed_str += " " + " ".join(map(str, self.totals["Percentile"]))

        return composed_str


@dataclass()
class DicePool:
    @staticmethod
    def default_dice() -> Dict[Dice, int]:
        d = {}

        for die_type in Dice:
            d[die_type] = 0

        return d

    @staticmethod
    def dict_factory(dict_src: List[Tuple[str, Any]]) -> Dict[str, Any]:
        """
        We don't want to export dice_counts, internal use only
        """
        dict_dest: Dict[str, Any] = {
            "name": None,
            "dice": None,
            "description": None,
        }

        for key, value in dict_src:
            if key in dict_dest:
                if is_dataclass(value) and not isinstance(value, type):
                    dict_dest[key] = asdict(value)
                else:
                    dict_dest[key] = value

        return dict_dest

    dice: str = ""
    name: str = ""
    description: str = ""
    additional_effects: List["AdditionalEffectOption"] = field(default_factory=list)
    dice_counts: Dict[Dice, int] = field(default_factory=default_dice, init=False)

    def __post_init__(self) -> None:
        self.set_dice(self.dice)

    def asdict(self) -> Dict[str, Any]:
        return asdict(self, dict_factory=DicePool.dict_factory)

    def count(self) -> int:
        return len(self.dice)

    def set_dice(self, dice_str: str) -> Self:
        for die_type in get_dice_from_str(dice_str):
            self.dice_counts[die_type] += 1

        return self

    def modify(self, die_type: Dice, modifier: Optional[Modifier] = None) -> Self:
        match modifier:
            case Modifier.ADD:
                self.dice_counts[die_type] += 1
            case Modifier.UPGRADE:
                if die_type.upgrade and self.dice_counts[die_type] > 0:
                    self.dice_counts[die_type] -= 1
                    self.dice_counts[die_type.upgrade] += 1
                else:
                    self.dice_counts[die_type] += 1
            case Modifier.REMOVE:
                if self.dice_counts[die_type] > 0:
                    self.dice_counts[die_type] -= 1
            case Modifier.DOWNGRADE:
                if self.dice_counts[die_type] > 0:
                    if die_type.downgrade:
                        self.dice_counts[die_type] -= 1
                        self.dice_counts[die_type.downgrade] += 1
                    else:
                        self.dice_counts[die_type] -= 1
            case _:
                pass

        self.dice = self.roll_str()

        return self

    def add_additional_effect(self, effect: "AdditionalEffectOption") -> None:
        for die_type in effect.dice:
            self.modify(die_type, effect.modifier)

        self.additional_effects.append(effect)

    def remove_additional_effect(self, effect: "AdditionalEffectOption") -> None:
        for die_type in effect.dice:
            self.modify(die_type, effect.modifier.opposite)

        self.additional_effects.remove(effect)

    def roll(self) -> Result:
        roll_result = Result()

        for die_type in self.get_dice():
            die_result: DieResult = die_type.roll()
            roll_result.add(die_result)

        return roll_result.reduce()

    def get_dice(self, keys: Optional[List[Dice]] = None) -> List[Dice]:
        """
        Get all dice as a list.  If keys is supplied, only get the dice for
        those keys.
        """
        dice = []

        if keys is not None:
            dice_items = {
                k: v for k, v in self.dice_counts.items() if k in keys
            }.items()
        else:
            dice_items = self.dice_counts.items()

        for die_type, count in dice_items:
            for _ in range(1, count + 1):
                dice.append(die_type)

        return dice

    def get_dice_faces(self) -> List[List[Face]]:
        faces = []

        for die_type in self.get_dice():
            faces.append(die_type.faces)

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

            if Symbol.SUCCESS.unicode in r:
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
            composed_str += die_type.short_code * count

        return composed_str

    def is_empty(self) -> bool:
        return sum(self.dice_counts.values()) == 0

    def to_foundry_str(self) -> str:
        macro_args = []

        foundry_dice = []

        for die_type, count in self.dice_counts.items():
            if die_type is Dice.PERCENTILE:
                continue

            foundry_code = die_type.foundry
            foundry_dice.append(f"{count}{foundry_code}")

        macro_args.append("roll=" + "+".join(foundry_dice))

        if len(self.name) > 0:
            escaped_name = self.name.strip().replace(" ", "|")
            macro_args.append(f"title={escaped_name}")

        if len(self.description) > 0:
            escaped_description = (
                self.description.strip().replace(" ", "|").replace("\n", "\\n")
            )
            macro_args.append(f"description={escaped_description}")

        macro_str = "/macro dice " + " ".join(macro_args)

        return macro_str

    def __str__(self) -> str:
        return self.dice


@dataclass(eq=True, frozen=True)
class AdditionalEffectOption:
    name: str
    description: str
    difficulty: str
    modifier: Modifier = field(init=False)
    dice: List[Dice] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        prefix = self.difficulty[0]
        match prefix:
            case "-":
                mod, index = Modifier.REMOVE, 1
            case "+":
                mod, index = Modifier.ADD, 1
            case _ if DiceShortCode.exists(prefix):
                mod, index = Modifier.ADD, 0
            case _:
                raise Exception(f"Invalid prefix or short code: {prefix}")

        object.__setattr__(self, "modifier", mod)
        dice_str = self.difficulty[index:]

        for die_str in dice_str:
            self.dice.append(Dice.from_short_code(die_str))

    def __hash__(self) -> int:
        return hash((self.name, self.description, self.difficulty))


@dataclass
class AdditionalEffects:
    name: str
    options: List[AdditionalEffectOption]

    def max_difficulty_len(self) -> int:
        return max(*list(map(len, [o.difficulty for o in self.options])))


additional_effects: Dict[str, AdditionalEffects] = {}


def add_additional_effects(effects: AdditionalEffects) -> None:
    if effects.name in additional_effects:
        raise Exception(f"Effects with name {effects.name} already exists!")

    additional_effects[effects.name] = effects


def get_dice_from_str(dice_str: str) -> List[Dice]:
    dice = []
    for die_str in dice_str.strip().upper():
        if DiceShortCode.exists(die_str):
            dice.append(Dice.from_short_code(die_str))
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

    for die_type in [
        Dice.BOOST,
        Dice.SETBACK,
        Dice.ABILITY,
        Dice.DIFFICULTY,
        Dice.PROFICIENCY,
        Dice.CHALLENGE,
    ]:
        row = [die_type.name]
        for face in die_type.faces:
            if type(face) is list:
                row.append(" ".join([f.unicode for f in face]))
            else:
                symbol = cast(Symbol, face)
                row.append(symbol.unicode)
        table.append(row)

    return table
