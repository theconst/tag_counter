import argparse
import sys
from typing import Union

import log
from model.entities import Site
from model.tag_counter_model import TagCounterModel
from tag_counter_view import TagCounterView

logger = log.get_logger(__name__)


class ConsoleTagCounterView(TagCounterView):
    """Console view for tag counter"""

    def __init__(self, tag_counter_model: TagCounterModel):
        TagCounterView.__init__(self, tag_counter_model)

        self._tag_counter_model.on_site_refreshed += self._print_table
        self._tag_counter_model.on_error += self._print_error

    def activate(self):
        parser = argparse.ArgumentParser(description='Application for counting tags on websites')

        parser.add_argument(
            '--get',
            type=str,
            dest='get_url',
            help='URL or alias of the site to count tags on')
        parser.add_argument(
            '--view',
            type=str,
            dest='view_url',
            help='URL or alias of the site to count tags on')
        parser.add_argument(
            '--alias-file',
            dest='alias',
            type=str,
            help='Path to yaml file with site aliases')

        args = parser.parse_args()

        alias, get_url, view_url = args.alias, args.get_url, args.view_url

        if get_url:
            self.on_refresh_selected(True)
            self.on_input_submitted(get_url)
        elif view_url:
            self.on_refresh_selected(False)
            self.on_input_submitted(view_url)

        if alias:
            self.on_input_file_selected(alias)

    def _print_table(self, site: Site):
        print(site.tag_histogram.table())

    def _print_error(self, error: Union[str, Exception]):
        print(error, file=sys.stderr)
