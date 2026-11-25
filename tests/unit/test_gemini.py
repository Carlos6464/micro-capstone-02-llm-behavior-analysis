import json
from unittest.mock import MagicMock

import pytest

from src.core.config import ExperimentConfig
from src.core.schemas import LLMMessage
from src.providers.factory import create_provider


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Valida requisição e contabilização Gemini sem rede.
@pytest.mark.parametrize("judge,prefix", [(False, "LLM"), (True, "JUDGE")])
def test_gemini(monkeypatch, judge, prefix):
    monkeypatch.setenv(f"{prefix}_PROVIDER", "gemini")
    monkeypatch.setenv(f"{prefix}_API_KEY", "fake")
    monkeypatch.setenv(f"{prefix}_MODEL", "gemini-2.5-flash")
    provider = create_provider(ExperimentConfig(), judge=judge)
    response = {
        "candidates": [{"finishReason": "STOP", "content": {"parts": [{"text": "OK"}]}}],
        "usageMetadata": {"promptTokenCount": 10, "candidatesTokenCount": 2, "thoughtsTokenCount": 1},
    }
    sender = MagicMock()
    sender.return_value.__enter__.return_value.read.return_value = json.dumps(response)
    monkeypatch.setattr("src.providers.gemini_provider.urlopen", sender)
    messages = [
        LLMMessage(role="system", content="Política"),
        LLMMessage(role="user", content="Pergunta"),
    ]
    result = provider.generate(messages)
    assert (result.text, result.input_tokens, result.output_tokens) == ("OK", 10, 3)
    payload = json.loads(sender.call_args.args[0].data)
    assert payload["systemInstruction"]["parts"][0]["text"] == "Política"
    assert payload["contents"][0]["parts"][0]["text"] == "Pergunta"
    assert payload["generationConfig"]["temperature"] == (0.0 if judge else 0.2)
    if judge:
        assert payload["generationConfig"]["responseMimeType"] == "application/json"
    response["candidates"][0]["finishReason"] = "MAX_TOKENS"
    sender.return_value.__enter__.return_value.read.return_value = json.dumps(response)
    with pytest.raises(ValueError):
        provider.generate(messages)
    response["candidates"][0]["finishReason"] = "STOP"
    response["candidates"][0]["content"]["parts"] = []
    sender.return_value.__enter__.return_value.read.return_value = json.dumps(response)
    with pytest.raises(ValueError):
        provider.generate(messages)
