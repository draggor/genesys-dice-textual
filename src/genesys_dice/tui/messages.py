from typing import Any, Optional

from textual.message import Message

from genesys_dice.dice import DicePool


class ModalMessage(Message):
    def __init__(self, screen, data: Any):
        self.screen = screen
        self.data = data
        super().__init__()


# class SwitchTabMessage[T](Message):
#    def __init__(self, destination: str, dice: Optional[T]) -> None:
#        super().__init__()
#        self.destination = destination
#        self.dice = dice


class SwitchTabMessage(Message):
    def __init__(self, destination: str, dice: Optional[DicePool]) -> None:
        super().__init__()
        self.destination = destination
        self.dice = dice
