import os
import unittest
from urllib.parse import urlunsplit

from tagcounter.model.tag_parser import CollectingTagParser
from tests.test_stubs import HTML_STRING
from tests.test_stubs import HTML_STRING_TAGS

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


class TagParserTest(unittest.TestCase):

    def test_extraction_of_tags_from_single_html_file(self):
        sut = CollectingTagParser()
        sut.feed(HTML_STRING)

        actual = sut.tags

        self.assertEqual(HTML_STRING_TAGS, actual)

    def test_extraction_of_html_tags_by_lines(self):
        sut = CollectingTagParser()
        lines = HTML_STRING.splitlines()
        first_line, *other_lines = lines

        sut.feed(first_line)
        self.assertEqual(HTML_STRING_TAGS[0:1], sut.tags)

        for line in other_lines:
            sut.feed(line)
        self.assertEqual(HTML_STRING_TAGS, sut.tags)

    def test_clear_tags(self):
        sut = CollectingTagParser()

        sut.feed(HTML_STRING)

        self.assertEqual(HTML_STRING_TAGS, sut.tags)

        sut.clear_tags()

        self.assertEqual([], sut.tags)

    def test_parse_string_iterator(self):
        def stub_iterator():
            yield '<p>'
            yield 'Line</br>'

        actual = list(CollectingTagParser.parse(stub_iterator()))

        self.assertEqual(['p', 'br'], actual)

    def test_parse_string(self):
        actual = list(CollectingTagParser.parse(HTML_STRING))

        self.assertEqual(HTML_STRING_TAGS, actual)

    def test_parse_from_url(self):
        test_file_path = os.path.join(SCRIPT_DIR, 'test_file.html')
        url = urlunsplit(('file', '', test_file_path, '', ''))

        actual = list(CollectingTagParser.parse_url(url))

        self.assertEqual(['html', 'body', 'p', 'p', 'br', 'body', 'html'], actual)
