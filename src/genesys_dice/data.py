import os
from typing import List, Optional, TypeVar

from dataclass_wizard import fromdict  # type: ignore

from platformdirs import PlatformDirs

from rich.pretty import pprint

import yaml

from genesys_dice.dice import (
    DicePool,
    AdditionalEffects,
)

PLATFORM_DIRS = PlatformDirs("genesys-dice")
DATA_FILE_NAME = "genesys-dice-saved-rolls.yaml"


def resource_path(relative: str) -> str:
    return os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), relative))
    )


def _load_from_file(path: Optional[str] = None) -> List[DicePool]:
    if path is not None:
        data_file_path = resource_path(path)
    else:
        data_file_path = os.path.join(PLATFORM_DIRS.user_data_dir, DATA_FILE_NAME)

    with open(data_file_path, "r") as file:
        data = yaml.safe_load(file)

    parsed_data = []

    for item in data:
        saved_roll = DicePool(**item)
        parsed_data.append(saved_roll)

    return parsed_data


T = TypeVar("T")


def load_from_file(path: str, cls: type[T]) -> List[T]:
    data_file_path = resource_path(path)

    with open(data_file_path, "r") as file:
        data = yaml.safe_load(file)

    parsed_data = []

    for item in data:
        # instance = cls(**item)
        instance = fromdict(cls, item)
        parsed_data.append(instance)

    return parsed_data


def main() -> None:
    # print(
    #    yaml.dump(
    #        [
    #            DicePool(name="A test roll", dice="PAADD").asdict(),
    #            DicePool(
    #                name="Another one", dice="AAD", description="Whatever yo"
    #            ).asdict(),
    #        ],
    #        sort_keys=False,
    #    )
    # )
    # pprint(load_from_file("test-data.yaml"))
    # load_additional_effects()
    # pprint(additional_effects)
    items = load_from_file("roll-builders.yaml", AdditionalEffects)
    # items = load_from_file("test-data.yaml", DicePool)
    pprint(items)


if __name__ == "__main__":
    main()
