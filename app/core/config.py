from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVER_PORT: int
    SERVER_HOST: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_setting():
    return Settings()
