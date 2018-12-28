from unittest import TestCase
from unittest.mock import patch

from event import event
from model import alias_storage, db
# Mock out decorators
from model.entities import Site


def mock_transactional(_, func):
    return func


db.DataAccessLayer.transactional = mock_transactional


def mock_catch_as(_):
    def wrapper(f):
        return f
    return wrapper


event.catch_as = mock_catch_as

from model.tag_counter_model import TagCounterModel


class TestTagCounterModel(TestCase):

    def setUp(self):
        self.sut = TagCounterModel(alias_storage.empty)

    def test_selected_site(self):
        expected = 'https://site.com'

        self.sut.selected_site_url = expected

        self.assertEqual(expected, self.sut.selected_site_url)

    @patch('model.site_repository.load_all_sites')
    def test_load_all_sites(self, mock_load_all):
        site_list = [Site('https://site1'), Site('https://site2'), Site('https://site3')]
        mock_load_all.return_value = site_list

        actual_loaded_sites = []
        self.sut.on_url_added += lambda url: actual_loaded_sites.append(url)

        self.sut.load_all_sites(None)

        self.assertEqual([s.url for s in site_list], actual_loaded_sites)

    def test_fail_on_load_unselected_site(self):
        with patch.object(self.sut, 'on_error', wraps=self.sut.on_error) as on_error:
            self.sut.load_selected_site(None)

            on_error.assert_called_with('Site is not selected')

    def test_fail_on_refresh_unselected_site(self):
        with patch.object(self.sut, 'on_error', wraps=self.sut.on_error) as on_error:
            self.sut.refresh_selected_site(None)

            on_error.assert_called_with('Site URL is not defined')

    @patch('validators.url')
    def test_fail_on_load_invalid_site(self, mock_validator):
        mock_validator.return_value = False
        self.sut.selected_site_url = 'some.url'
        with patch.object(self.sut, 'on_error', wraps=self.sut.on_error) as on_error:
            self.sut.refresh_selected_site(None)

            on_error.assert_called_with('Site URL is invalid')

    @patch('model.site_repository.load_site_by_url')
    def test_load_selected_site(self, mock_load_site):
        site = Site('https://site.com')
        mock_load_site.return_value = site

        self.sut.selected_site_url = site.url

        with patch.object(self.sut, 'on_site_refreshed', wraps=self.sut.on_site_refreshed) as on_refresh:
            self.sut.load_selected_site(None)

            on_refresh.assert_called_with(site=site)

    @patch('model.site_repository.save_or_update')
    @patch('model.tag_parser.CollectingTagParser.parse_url')
    def test_refresh_selected_site(self, mock_parse_url, mock_save_or_update):
        site = Site('https://nonexisitingsite.com')

        mock_parse_url.return_value = ['a', 'b']
        mock_save_or_update.return_value = site

        self.sut.selected_site_url = site.url

        with patch.object(self.sut, 'on_url_added', wraps=self.sut.on_url_added) as on_url_added,\
                patch.object(self.sut, 'on_site_refreshed', wrpas=self.sut.on_site_refreshed) as on_site_refreshed:
            self.sut.refresh_selected_site(None)

            mock_parse_url.assert_called_with(site.url)

            mock_save_or_update.asser_called_once()
            on_url_added.assert_called_with(url=site.url)
            on_site_refreshed.assert_called_once()

            self.assertEqual(on_url_added.call_args[1]['url'], site.url)
            self.assertEqual(on_site_refreshed.call_args[1]['site'], site)

    def test_default_alias_file(self):
        self.assertIsNone(self.sut.alias_file)

    @patch('model.alias_storage.file_storage')
    def test_load_alias_storage_on_update(self, mock_storage_factory):
        mock_storage_factory.return_value = alias_storage.empty
        file = 'new_file.yml'

        self.sut.alias_file = file

        self.assertEqual(file, self.sut.alias_file)

        mock_storage_factory.assert_called_with(file)
