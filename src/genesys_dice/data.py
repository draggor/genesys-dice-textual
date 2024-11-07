from dataclasses import asdict, dataclass
import os
from typing import List, Optional

from platformdirs import PlatformDirs

from rich.pretty import pprint

import yaml


PLATFORM_DIRS = PlatformDirs("genesys-dice")
DATA_FILE_NAME = "genesys-dice-saved-rolls.yaml"


def load_from_file(path: Optional[str] = None):
    if path is not None:
        data_file_path = path
    else:
        data_file_path = os.path.join(PLATFORM_DIRS.user_data_dir, DATA_FILE_NAME)

    with open(data_file_path, "r") as file:
        data = yaml.safe_load(file)

    return data


@dataclass
class SavedRoll:
    name: str
    dice: str
    description: Optional[str] = None

    @staticmethod
    def load_from_file(path: Optional[str] = None) -> List["SavedRoll"]:
        if path is not None:
            data_file_path = path
        else:
            data_file_path = os.path.join(PLATFORM_DIRS.user_data_dir, DATA_FILE_NAME)

        with open(data_file_path, "r") as file:
            data = yaml.safe_load(file)

        parsed_data = []

        for item in data:
            saved_roll = SavedRoll(**item)
            parsed_data.append(saved_roll)

        return parsed_data


def main() -> None:
    print(
        yaml.dump(
            [
                asdict(SavedRoll("A test roll", "PAADD")),
                asdict(SavedRoll("Another one", "AAD", description="Whatever yo")),
            ],
            sort_keys=False,
        )
    )
    pprint(SavedRoll.load_from_file("test-data.yaml"))


if __name__ == "__main__":
    main()
