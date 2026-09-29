from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str = ""

    gemini_flash_model: str = "gemini-2.5-flash-lite"

    gemini_pro_model: str = "gemini-2.5-flash-lite"

    image_provider: str = "placeholder"

    hf_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()