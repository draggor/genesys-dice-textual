from typing import Any, Optional

from textual.message import Message
from textual.screen import Screen

from genesys_dice.dice import DicePool


class DicePoolMessage(Message):
    def __init__(self, dice_pool: DicePool) -> None:
        super().__init__()
        self.dice_pool = dice_pool


class CopyCommandMessage(DicePoolMessage):
    pass


class ModalMessage(Message):
    def __init__(self, screen: Screen[None], data: Any):
        self.screen = screen
        self.data = data
        super().__init__()


class SaveRollMessage(DicePoolMessage):
    pass


class SwitchTabMessage(Message):
    def __init__(self, destination: str, dice_pool: Optional[DicePool]) -> None:
        super().__init__()
        self.destination = destination
        self.dice_pool = dice_pool
