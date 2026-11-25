from src.core.schemas import LLMMessage
from src.providers.base import ProviderResponse


class OpenAIProvider:
    def __init__(self, client, model: str, temperature: float, top_p: float,
                 max_output_tokens: int):
        self.client = client
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.max_output_tokens = max_output_tokens

    def generate(self, messages: list[LLMMessage]) -> ProviderResponse:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[message.model_dump() for message in messages],
            temperature=self.temperature,
            top_p=self.top_p,
            max_completion_tokens=self.max_output_tokens,
        )
        choice = response.choices[0]
        if choice.finish_reason != "stop" or not choice.message.content:
            raise ValueError("Resposta incompleta ou vazia.")
        usage = response.usage
        return ProviderResponse(
            choice.message.content, response.model,
            usage.prompt_tokens if usage else None,
            usage.completion_tokens if usage else None,
            response.id,
        )
