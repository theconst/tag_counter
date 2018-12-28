import log
import sys
from html.parser import HTMLParser
from typing import List, Iterable, Union, overload
from urllib.request import urlopen

log = log.get_logger(__name__)


class ParserError(Exception):
    """ Error raised during parsing """

    def __init__(self, message):
        super().__init__(message)


class CollectingTagParser(HTMLParser):
    """ Parser that collects tags and allows to flush computed tags when not necessary """

    def __init__(self):
        super().__init__()
        self._tags = []

    def error(self, message):
        raise ParserError(message)

    def handle_starttag(self, tag, attrs):
        self._tags.append(tag)

    def handle_endtag(self, tag):
        self._tags.append(tag)

    def clear_tags(self):
        self._tags = []
        self.reset()

    @property
    def tags(self) -> List[str]:
        return self._tags

    @staticmethod
    @overload
    def parse(html: str) -> Iterable[str]:
        ...

    @staticmethod
    @overload
    def parse(html: Iterable[str]) -> Iterable[str]:
        ...

    @staticmethod
    def parse(html: Union[str, Iterable[str]]) -> Iterable[str]:
        """
        Parses tags inside stream of documents or
        :param html: string(s) to parse
        :return: stream of tags
        """

        if type(html) is str:
            # behave sanely if string is supplied
            return (yield from CollectingTagParser.parse([html]))

        parser = CollectingTagParser()
        for s in html:
            parser.feed(s)
            yield from parser.tags
            parser.clear_tags()

    @staticmethod
    def parse_url(url: str, encoding: str = sys.getdefaultencoding()) -> Iterable[str]:
        """
        Parse from url

        :param url: url to parse
        :param encoding: encoding to use
        :return: sequence of tags for the site
        """
        with urlopen(url) as stream:
            response_byte_stream = stream.read()
            response_char_stream = response_byte_stream.decode(encoding)
            return CollectingTagParser.parse(response_char_stream)
