from typing import Iterable, Optional
from config import Config
from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import User
import asyncio


class APIManager:
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
