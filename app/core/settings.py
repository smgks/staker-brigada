import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsConf(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: int
    DB_DRIVER: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 240
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    def get_db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


Settings = SettingsConf()
