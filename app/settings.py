from os import getenv
from typing import Dict

from utils.secrets import SecretFetcher


class Settings:
    def __init__(self):
        self._secret_fetcher = SecretFetcher(
            aws_access_key=getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_key=getenv("AWS_SECRET_ACCESS_KEY"),
            aws_region=getenv("AWS_REGION"),
        )
        self._secrets_cache = {}

    def _fetch_secret(self, secret_name: str) -> Dict:
        """
        Завантажує секрет із AWS або повертає його з кешу.
        """
        if secret_name not in self._secrets_cache:
            self._secrets_cache[secret_name] = self._secret_fetcher.fetch_secret(
                secret_name
            )
        return self._secrets_cache[secret_name]

    @property
    def __database(self) -> Dict:
        return self._fetch_secret("dev/BookEasyBot")

    @property
    def __telegram_tokens(self) -> Dict:
        return self._fetch_secret("BookEasyBot/telegram_tokens")

    @property
    def main_token(self) -> str:
        return self.__telegram_tokens.get("main_bot_token")

    @property
    def sender_token(self) -> str:
        return self.__telegram_tokens.get("sender_bot_token")

    @property
    def database_url(self) -> str:
        db = self.__database
        return f"postgresql+asyncpg://{db.get('username')}:{db.get('password')}@{db.get('host')}:{db.get('port')}/{db.get('dbname')}"


settings = Settings()
