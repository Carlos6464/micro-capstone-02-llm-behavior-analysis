import json
from time import sleep
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from src.core.schemas import LLMMessage
from src.providers.base import ProviderResponse


class GeminiProvider:
    # Autor: Carlos Adriano
    # Data: 25/11/2026
    # Descrição: Configura o adaptador REST Gemini sem dependências adicionais.
    def __init__(self, key, model, temperature, top_p, max_output_tokens, *, judge=False):
        if model != "gemini-2.5-flash":
            raise ValueError("Modelo Gemini não homologado na configuração de preços.")
        self.key = key
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.max_output_tokens = max_output_tokens
        self.judge = judge

    # Autor: Carlos Adriano
    # Data: 25/11/2026
    # Descrição: Envia mensagens separadas e contabiliza tokens faturáveis.
    def generate(self, messages: list[LLMMessage]) -> ProviderResponse:
        system = [m.content for m in messages if m.role == "system"]
        contents = [
            {
                "role": "model" if m.role == "assistant" else "user",
                "parts": [{"text": m.content}],
            }
            for m in messages
            if m.role != "system"
        ]
        config = {
            "temperature": self.temperature,
            "topP": self.top_p,
            "maxOutputTokens": self.max_output_tokens,
            "thinkingConfig": {"thinkingBudget": 0},
        }
        if self.judge:
            config["responseMimeType"] = "application/json"
        payload = {"contents": contents, "generationConfig": config}
        if system:
            payload["systemInstruction"] = {"parts": [{"text": s} for s in system]}
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        )
        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "x-goog-api-key": self.key},
            method="POST",
        )
        for attempt in range(3):
            try:
                with urlopen(request, timeout=60) as response:
                    data = json.load(response)
                break
            except HTTPError as error:
                if error.code != 503 or attempt == 2:
                    raise
                sleep(15 * (2**attempt))
        candidates = data.get("candidates", [])
        if not candidates or candidates[0].get("finishReason") != "STOP":
            raise ValueError("Resposta Gemini bloqueada ou incompleta.")
        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
        if not text.strip():
            raise ValueError("Resposta Gemini vazia.")
        usage = data.get("usageMetadata", {})
        output = usage.get("candidatesTokenCount")
        if output is not None:
            output += usage.get("thoughtsTokenCount", 0)
        return ProviderResponse(
            text,
            data.get("modelVersion", self.model),
            usage.get("promptTokenCount"),
            output,
            data.get("responseId"),
        )
