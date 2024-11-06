from typing import Optional

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Placeholder


from genesys_dice.data import SavedRoll


class Templates(Container):

    def compose(self) -> ComposeResult:
        yield Placeholder(id="bees")

    def set_data[T](self, roll: Optional[T]) -> None:
        self.notify(str(roll))
