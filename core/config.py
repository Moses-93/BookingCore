from pydantic_settings import BaseSettings
from utils.secrets import SecretFetcher


class Settings(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._secret_fetcher = SecretFetcher(
            aws_access_key=self.aws_access_key_id,
            aws_secret_key=self.aws_secret_access_key,
            aws_region=self.aws_region,
        )

    @property
    def _database_secrets(self):
        return self._secret_fetcher.fetch_secret("dev/BookEasyBot")

    @property
    def _telegram_secrets(self):
        return self._secret_fetcher.fetch_secret("BookEasyBot/telegram_tokens")

    @property
    def telegram_main_token(self):
        return self._telegram_secrets.get("main_bot_token")

    @property
    def telegram_sender_token(self):
        return self._telegram_secrets.get("sender_bot_token")

    @property
    def database_url(self):
        db = self._database_secrets
        return f"postgresql+asyncpg://{db.get("username")}:{db.get("password")}@{db.get("host")}:{db.get("port")}/{db.get("dbname")}"


settings = Settings()
