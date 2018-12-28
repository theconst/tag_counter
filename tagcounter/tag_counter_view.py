import abc

from event.event import Event
from model.tag_counter_model import TagCounterModel


class TagCounterView(metaclass=abc.ABCMeta):
    _tag_counter_model: TagCounterModel

    def __init__(self, tag_counter_model: TagCounterModel) -> None:
        self._tag_counter_model = tag_counter_model

    def activate(self) -> None:
        """
        Method that activates view (shows window on the screen, parses options etc.).
        The call may block indefinetely as it requires user interaction
        """

    @Event
    def on_input_submitted(self, value: str) -> None:
        """Fired when user submits events"""

    @Event
    def on_refresh_selected(self, refresh: bool) -> None:
        """Fired when user selects refresh option for input"""

    @Event
    def on_input_file_selected(self, value: str) -> None:
        """Fired when user selects new alias file"""
