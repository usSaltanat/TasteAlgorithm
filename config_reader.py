from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    postgresql_database: str
    postgresql_username: str
    postgresql_password: str #SecretStr
    postgresql_hostname: str
    postgresql_port: str

    model_config = SettingsConfigDict(env_file=".env")


env_config = Settings()