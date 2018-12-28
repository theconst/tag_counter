import abc
from typing import Optional

import yaml
import log

from pkg_resources import resource_filename

import resources

logger = log.get_logger(__name__)


class AliasStorage:

    @abc.abstractmethod
    def __getattr__(self, item: str) -> str: ...

    @abc.abstractmethod
    def get(self, value, default=None) -> str: ...


class EmptyStorage(AliasStorage):

    def __getattr__(self, item: str) -> str:
        raise KeyError

    def get(self, value, default=None) -> str:
        return default


class YamlAliasStorage(AliasStorage):

    def __init__(self, alias_file: Optional[str] = None) -> None:
        try:
            alias_file_or_default = alias_file or resource_filename('resources', resources.ALIAS_FILE)
            with open(alias_file_or_default) as file:
                self._alias_to_site = yaml.safe_load(file)['Sites']
        except (KeyError, FileNotFoundError) as e:
            logger.warning('Failed to load alias file', e)
            self._alias_to_site = {}

    def __getattr__(self, value):
        return self._alias_to_site[value]

    def get(self, value, default=None):
        return self._alias_to_site.get(value, default)


empty = EmptyStorage()
default = YamlAliasStorage()


def file_storage(file_name: Optional[str] = None) -> AliasStorage:
    """Factory for alias storage"""
    return YamlAliasStorage(file_name)
