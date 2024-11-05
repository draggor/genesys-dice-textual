from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Placeholder


class Templates(Container):

    def compose(self) -> ComposeResult:
        yield Placeholder(id="bees")
