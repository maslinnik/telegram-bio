from typing import Iterable, Optional
from config import Config
from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import User
from abc import ABC, abstractmethod
import asyncio
from bs4 import BeautifulSoup
import requests


class APIManager(ABC):
    @abstractmethod
    def user_exists_batch(self, usernames: Iterable[str]) -> Iterable[bool]:
        pass

    @abstractmethod
    def user_exists(self, username: str) -> bool:
        pass

    @abstractmethod
    def get_bio_batch(self, usernames: Iterable[str]) -> Iterable[str]:
        pass

    @abstractmethod
    def get_bio(self, username: str) -> str:
        pass


class WebScraper(APIManager):
    def __get_tgme_soup(self, username: str) -> BeautifulSoup:
        r = requests.get(f'https://t.me/{username}')
        return BeautifulSoup(r.text, features="html.parser")

    def user_exists(self, username: str) -> bool:
        soup = self.__get_tgme_soup(username)
        name_obj = soup.find('div', {'class': 'tgme_page_title'})
        preview_obj = soup.find('div', {'class': 'tgme_page_context_link_wrap'})
        return name_obj is not None and preview_obj is None

    def get_bio(self, username: str) -> str:
        soup = self.__get_tgme_soup(username)
        name_obj = soup.find('div', {'class': 'tgme_page_title'})
        preview_obj = soup.find('div', {'class': 'tgme_page_context_link_wrap'})
        bio_obj = soup.find('div', {'class': 'tgme_page_description'})
        if name_obj is None or preview_obj is not None or bio_obj is None:
            return ''
        delimiter = '\0'
        for line_break in bio_obj.findAll('br'):
            line_break.replaceWith(delimiter)
        return bio_obj.text.replace(delimiter, '\n')

    def user_exists_batch(self, usernames: Iterable[str]) -> Iterable[bool]:
        return [self.user_exists(username) for username in usernames]

    def get_bio_batch(self, usernames: Iterable[str]) -> Iterable[str]:
        return [self.get_bio(username) for username in usernames]


class MTProtoAPIManager(APIManager):
    def user_exists_batch(self, usernames: Iterable[str]) -> Iterable[bool]:
        async def main():
            client = await (TelegramClient('session', Config.TG_API_ID, Config.TG_API_HASH)
                            .start(bot_token=Config.TG_BOT_TOKEN))
            result = []
            async with client:
                for username in usernames:
                    try:
                        entity = await client.get_entity(username)
                        result.append(isinstance(entity, User))
                    except ValueError:
                        result.append(False)
            return result
        return asyncio.run(main())

    def user_exists(self, username: str) -> bool:
        return next(iter(self.user_exists_batch([username])))

    def get_bio_batch(self, usernames: Iterable[str]) -> Iterable[str]:
        async def main():
            client = await (TelegramClient('session', Config.TG_API_ID, Config.TG_API_HASH)
                            .start(bot_token=Config.TG_BOT_TOKEN))
            result = []
            async with client:
                for username in usernames:
                    try:
                        full = await client(GetFullUserRequest(username))
                        result.append(full.full_user.about or '')
                    except ValueError:
                        result.append('')
            return result
        return asyncio.run(main())

    def get_bio(self, username: str) -> str:
        return next(iter(self.get_bio_batch([username])))
