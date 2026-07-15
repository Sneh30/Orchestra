import json
from typing import Any, Protocol

from research_orchestrator.core.config import Settings


class LLMProvider(Protocol):
    async def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
    ) -> dict[str, Any]:
        ...


class DeterministicLLMProvider:
    async def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
    ) -> dict[str, Any]:
        del system_prompt, temperature
        return {"raw_response": user_prompt}


class LangChainChatProvider:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
    ) -> dict[str, Any]:
        model = self._build_model(temperature)
        if isinstance(model, DeterministicLLMProvider):
            return await model.complete_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=temperature,
            )
        response = await model.ainvoke(
            [
                ("system", system_prompt),
                ("human", user_prompt),
            ]
        )
        content = response.content if isinstance(response.content, str) else json.dumps(response.content)
        return self._parse_json(content)

    def _build_model(self, temperature: float) -> Any:
        if self.settings.llm_provider == "anthropic":
            from langchain_anthropic import ChatAnthropic

            if not self.settings.anthropic_api_key:
                return DeterministicLLMProvider()
            return ChatAnthropic(
                model=self.settings.anthropic_model,
                api_key=self.settings.anthropic_api_key.get_secret_value(),
                temperature=temperature,
                timeout=self.settings.request_timeout_seconds,
            )

        from langchain_openai import ChatOpenAI

        if not self.settings.openai_api_key:
            return DeterministicLLMProvider()
        return ChatOpenAI(
            model=self.settings.openai_model,
            api_key=self.settings.openai_api_key.get_secret_value(),
            temperature=temperature,
            timeout=self.settings.request_timeout_seconds,
            model_kwargs={"response_format": {"type": "json_object"}},
        )

    @staticmethod
    def _parse_json(content: str) -> dict[str, Any]:
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            cleaned = cleaned.removeprefix("json").strip()
        return json.loads(cleaned)


def create_llm_provider(settings: Settings) -> LLMProvider:
    if settings.llm_provider == "deterministic":
        return DeterministicLLMProvider()
    return LangChainChatProvider(settings)
