from typing import Any

from textual.message import Message


class ModalMessage(Message):

    def __init__(self, screen, data: Any):
        self.screen = screen
        self.data = data
        super().__init__()
