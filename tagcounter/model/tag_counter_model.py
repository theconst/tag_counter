from typing import Union, MutableSet, List, Optional

import validators

import log
from event.event import Event, catch_as
import model.alias_storage as alias_storage
from model.db import dal
from model.entities import Site
from model.histogram import Histogram
import model.site_repository as site_repository
import model.tag_parser as parser

persistent_logger = log.get_persistent_logger(__name__)


class TagCounterModel:
    """Model class for tag counter application"""

    should_refresh_selected: bool = True

    _selected_site_url: str = None
    _alias_file: str = None
    _available_urls: MutableSet[str]

    _alias_storage: alias_storage.AliasStorage = alias_storage.default

    _loaded_sites: List[Site]

    def __init__(self, alias_storage: alias_storage.AliasStorage = None):
        super().__init__()

        self._available_urls = set()

        if alias_storage:
            self._alias_storage = alias_storage

    @Event
    def on_site_refreshed(self, site: Site) -> None:
        """Fired when site is refreshed"""
        
    @Event
    def on_url_added(self, url: str) -> None:
        """Fired when name is added"""

    @Event
    def on_message(self, msg: str) -> None:
        """Fired when message is received"""

    @Event
    def on_error(self, error: Union[str, Exception]) -> None:
        """Fired if error occurred"""

    @catch_as('on_error')
    @dal.transactional
    def load_all_sites(self, session) -> None:
        for s in site_repository.load_all_sites(session):
            if s not in self._available_urls:
                self._available_urls.add(s.url)
                self.on_url_added(s.url)

    @catch_as('on_error')
    @dal.transactional
    def load_selected_site(self, session) -> None:
        url = self._selected_site_url
        if not url:
            return self.on_error('Site is not selected')

        retrieved_site = site_repository.load_site_by_url(session=session, site_url=url)
        if not retrieved_site:
            return self.on_error('Site is not in database')

        persistent_logger.info(retrieved_site.url)
        self.on_site_refreshed(site=retrieved_site)

    @catch_as('on_error')
    @dal.transactional
    def refresh_selected_site(self, session) -> None:
        resolved_url = self._alias_storage.get(self._selected_site_url, self._selected_site_url)

        if not resolved_url:
            return self.on_error('Site URL is not defined')

        if not validators.url(resolved_url):
            return self.on_error('Site URL is invalid')

        try:
            tags = parser.CollectingTagParser.parse_url(resolved_url)
        except IOError:
            return self.on_error("Failed to load site")
        histogram = Histogram(tags)
        site = site_repository.save_or_update(session=session, site=Site(resolved_url, histogram))

        persistent_logger.info(site.url)

        if site.url not in self._available_urls:
            self._available_urls.add(site.url)
            self.on_url_added(url=site.url)
        self.on_site_refreshed(site=site)

    @property
    @catch_as('on_error')
    def selected_site_url(self) -> Optional[str]:
        return self._selected_site_url

    @property
    def alias_file(self) -> str:
        return self._alias_file

    @alias_file.setter
    @catch_as('on_error')
    def alias_file(self, value: str) -> None:
        self._alias_file = value
        self._alias_storage = alias_storage.file_storage(value)

    @selected_site_url.setter
    @catch_as('on_error')
    def selected_site_url(self, value: str) -> None:
        self._selected_site_url = value
