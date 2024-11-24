"""
These are wrappers around common widgets to allow
border_title and border_subtitle as kwargs
"""

from typing import Any

from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Label


class TitleButton(Button):

    def __init__(
        self, border_title: str = "", border_subtitle: str = "", *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.border_title = border_title
        self.border_subtitle = border_subtitle


class TitleContainer(Container):

    def __init__(
        self, border_title: str = "", border_subtitle: str = "", *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.border_title = border_title
        self.border_subtitle = border_subtitle


class TitleHorizontal(Horizontal):

    def __init__(
        self, border_title: str = "", border_subtitle: str = "", *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.border_title = border_title
        self.border_subtitle = border_subtitle


class TitleVertical(Vertical):

    def __init__(
        self, border_title: str = "", border_subtitle: str = "", *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.border_title = border_title
        self.border_subtitle = border_subtitle


class TitleLabel(Label):

    def __init__(
        self, border_title: str = "", border_subtitle: str = "", *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.border_title = border_title
        self.border_subtitle = border_subtitle
