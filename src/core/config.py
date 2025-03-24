from pydantic_settings import BaseSettings
from src.utils.secrets import SecretFetcher


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
        return self._secret_fetcher.fetch_secret("dev/BookEasyBot/postgres")

    @property
    def _telegram_secrets(self):
        return self._secret_fetcher.fetch_secret("BookEasyBot/telegram_tokens")

    @property
    def _api_token(self):
        return self._secret_fetcher.fetch_secret("dev/BookEasyBot/API_TOKEN")

    @property
    def _payment_data(self) -> dict:
        return self._secret_fetcher.fetch_secret("payment_test_data")

    @property
    def api_token(self):
        return self._api_token.get("API_TOKEN")

    @property
    def telegram_main_token(self):
        return self._telegram_secrets.get("main_bot_token")

    @property
    def telegram_sender_token(self):
        return self._telegram_secrets.get("sender_bot_token")

    def database_url(self, driver="asyncpg"):
        db = self._database_secrets
        return f"postgresql+{driver}://{db.get("username")}:{db.get("password")}@{db.get("host")}:{db.get("port")}/{db.get("dbname")}"

    @property
    def redis_url(self):
        return "redis://localhost:6379/0"

    @property
    def merchant_secret_key(self):
        return self._payment_data.get("merchant_secret_key")

    @property
    def merchant_account(self):
        return self._payment_data.get("merchant_account")


settings = Settings()
