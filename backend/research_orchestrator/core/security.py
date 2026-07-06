from fastapi import Header

from research_orchestrator.core.config import Settings
from research_orchestrator.core.exceptions import UnauthorizedError


async def verify_api_key(
    settings: Settings,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> None:
    if not settings.api_key:
        return
    expected = settings.api_key.get_secret_value()
    if x_api_key != expected:
        raise UnauthorizedError()

