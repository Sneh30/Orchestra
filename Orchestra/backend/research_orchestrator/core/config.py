from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: Literal["local", "test", "staging", "production"] = "local"
    service_name: str = "multi-agent-research-orchestrator"
    log_level: str = "INFO"
    api_key: SecretStr | None = None

    database_url: str = "postgresql+asyncpg://research:research@localhost:5432/research_orchestrator"

    openai_api_key: SecretStr | None = None
    anthropic_api_key: SecretStr | None = None
    tavily_api_key: SecretStr | None = None
    llm_provider: Literal["openai", "anthropic", "deterministic"] = "openai"
    openai_model: str = "gpt-4.1-mini"
    anthropic_model: str = "claude-3-5-sonnet-latest"

    max_graph_iterations: int = Field(default=3, ge=1, le=8)
    default_max_sources: int = Field(default=12, ge=3, le=50)
    default_min_confidence: float = Field(default=0.72, ge=0.0, le=1.0)
    request_timeout_seconds: int = Field(default=60, ge=5, le=300)

    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()

