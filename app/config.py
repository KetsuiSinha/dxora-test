import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM
    openai_api_key: str | None = None
    gemini_api_key: str | None = None
    anthropic_api_key: str | None = None

    # Posting platforms
    twitter_api_key: str | None = None
    twitter_api_secret: str | None = None
    twitter_access_token: str | None = None
    twitter_access_token_secret: str | None = None
    twitter_bearer_token: str | None = None

    linkedin_access_token: str | None = None

    facebook_access_token: str | None = None
    facebook_page_id: str | None = None

    instagram_access_token: str | None = None
    instagram_business_account_id: str | None = None

    reddit_client_id: str | None = None
    reddit_client_secret: str | None = None
    reddit_username: str | None = None
    reddit_password: str | None = None
    reddit_user_agent: str = "dxora-test/1.0"

    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None

    devto_api_key: str | None = None
    medium_access_token: str | None = None

    # App
    app_host: str = "0.0.0.0"
    app_port: int = 4000
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
