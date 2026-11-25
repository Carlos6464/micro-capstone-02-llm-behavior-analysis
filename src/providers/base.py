from typing import Protocol
from dataclasses import dataclass

from src.core.schemas import LLMMessage


@dataclass(frozen=True)
class ProviderResponse:
    text: str
    model: str
    input_tokens: int | None
    output_tokens: int | None
    request_id: str | None = None


class LLMProvider(Protocol):
    # Autor: Carlos Adriano
    # Data: 25/11/2026
    # Descrição: Define o contrato de geração de respostas do provedor.
    def generate(self, messages: list[LLMMessage]) -> ProviderResponse: ...
