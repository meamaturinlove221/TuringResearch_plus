"""Settings for TulingResearch Core."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CoreSettings(BaseSettings):
    """Local settings for the minimal Core tool loop."""

    model_config = SettingsConfigDict(env_prefix="TULINGRESEARCH_", extra="ignore")

    cache_dir: Path = Field(default=Path(".tulingresearch/cache"))
    session_registry_path: Path = Field(default=Path(".tulingresearch/session_registry.json"))


def get_settings() -> CoreSettings:
    """Return Core settings from environment defaults."""

    return CoreSettings()
