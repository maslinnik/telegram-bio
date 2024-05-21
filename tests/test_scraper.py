from app.api_managers import WebScraper
from mock import patch, Mock
from requests import Response
from bs4 import BeautifulSoup
from test_model import TestCaseModel


class TestWebScraper(TestCaseModel):
    @patch('requests.get')
    def test_get_soup(self, request_call: Mock):
        request_call.return_value = Response()
        scraper = WebScraper()
        scraper._get_tgme_soup("username")
        request_call.assert_called_once_with("https://t.me/username")

    @patch('app.api_managers.WebScraper._get_tgme_soup')
    def test_user_exists(self, soup_call: Mock):
        text = '<div class="tgme_page_title"></div>'
        soup_call.return_value = BeautifulSoup(text, features="html.parser")
        scraper = WebScraper()
        self.assertTrue(scraper.user_exists("username"))
        soup_call.assert_called_once_with("username")

    @patch('app.api_managers.WebScraper._get_tgme_soup')
    def test_channel_exists(self, soup_call: Mock):
        text = ('<div class="tgme_page_title"></div>'
                '<div class="tgme_page_context_link_wrap"></div>')
        soup_call.return_value = BeautifulSoup(text, features="html.parser")
        scraper = WebScraper()
        self.assertFalse(scraper.user_exists("username"))
        soup_call.assert_called_once_with("username")

    @patch('app.api_managers.WebScraper._get_tgme_soup')
    def test_get_bio(self, soup_call: Mock):
        text = ('<div class="tgme_page_title"></div>'
                '<div class="tgme_page_description">some bio</div>')
        soup_call.return_value = BeautifulSoup(text, features="html.parser")
        scraper = WebScraper()
        self.assertEqual(scraper.get_bio("username"), "some bio")
        soup_call.assert_called_once_with("username")

    @patch('app.api_managers.WebScraper.user_exists')
    def test_get_bio_batch(self, bio_call: Mock):
        bio_call.side_effect = [True, False]
        scraper = WebScraper()
        self.assertEqual(scraper.user_exists_batch(["username", "losername"]),
                         [True, False])

    @patch('app.api_managers.WebScraper.get_bio')
    def test_get_bio_batch(self, bio_call: Mock):
        bio_call.side_effect = ["some bio", "another bio"]
        scraper = WebScraper()
        self.assertEqual(scraper.get_bio_batch(["username", "losername"]),
                         ["some bio", "another bio"])

