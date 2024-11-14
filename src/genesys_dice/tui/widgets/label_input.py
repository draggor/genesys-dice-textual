from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Input, Label, TextArea


class LabelInput(Vertical):

    DEFAULT_CSS = """
    LabelInput {
        Label {
            padding: 0 1;
        }
    }
    """

    def __init__(
        self,
        label_args=None,
        label_kwargs=None,
        input_args=None,
        input_kwargs=None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.label_args = [] if label_args is None else label_args
        self.label_kwargs = {} if label_kwargs is None else label_kwargs
        self.input_args = [] if input_args is None else input_args
        self.input_kwargs = {} if input_kwargs is None else input_kwargs

    def compose(self) -> ComposeResult:
        yield Label(*self.label_args, **self.label_kwargs)
        yield Input(*self.input_args, **self.input_kwargs)


class LabelTextArea(Vertical):

    DEFAULT_CSS = """
    LabelTextArea {
        Label {
            padding: 0 1;
        }
    }
    """

    def __init__(
        self,
        label_args=None,
        label_kwargs=None,
        text_area_args=None,
        text_area_kwargs=None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.label_args = [] if label_args is None else label_args
        self.label_kwargs = {} if label_kwargs is None else label_kwargs
        self.text_area_args = [] if text_area_args is None else text_area_args
        self.text_area_kwargs = {} if text_area_kwargs is None else text_area_kwargs

    def compose(self) -> ComposeResult:
        yield Label(*self.label_args, **self.label_kwargs)
        yield TextArea(*self.text_area_args, **self.text_area_kwargs)
