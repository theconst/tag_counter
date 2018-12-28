#!/usr/bin/env python3

import log
from model.tag_counter_model import TagCounterModel
from tag_counter_view import TagCounterView

logger = log.get_logger(__name__)


class TagCounterController:

    def __init__(self, counter_model: TagCounterModel, counter_view: TagCounterView):
        super().__init__()

        self._counter_model = counter_model
        self._counter_view = counter_view

        self._counter_view.on_input_submitted += self.load_site
        self._counter_view.on_refresh_selected += self.toggle_refresh
        self._counter_view.on_input_file_selected += self.select_alias_file

    def select_alias_file(self, value: str) -> None:
        self._counter_model.alias_file = value

    def load_site(self, value: str) -> None:
        self._counter_model.selected_site_url = value
        if self._counter_model.should_refresh_selected:
            self._counter_model.refresh_selected_site()
        else:
            self._counter_model.load_selected_site()

    def toggle_refresh(self, refresh: bool):
        self._counter_model.should_refresh_selected = refresh

    def run(self):
        self._counter_model.load_all_sites()
        self._counter_view.activate()
