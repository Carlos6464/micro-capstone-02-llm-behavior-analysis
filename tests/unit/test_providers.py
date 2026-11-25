from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from src.core.config import ExperimentConfig
from src.core.schemas import LLMMessage
from src.providers.factory import create_provider
from src.providers.openai_provider import OpenAIProvider


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Valida o adaptador sem acessar a API.
@pytest.mark.parametrize("finish,content,valid", [("stop", "OK", True), ("length", "", False)])
def test_provider(finish, content, valid):
    client = Mock()
    client.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(finish_reason=finish, message=SimpleNamespace(content=content))],
        usage=SimpleNamespace(prompt_tokens=10, completion_tokens=2),
        model="fake",
        id="fake-id",
    )
    provider = OpenAIProvider(client, "fake", 0.2, 1, 100)
    messages = [LLMMessage(role="user", content="Teste")]
    if valid:
        result = provider.generate(messages)
        assert (result.text, result.input_tokens, result.output_tokens) == ("OK", 10, 2)
        assert client.chat.completions.create.call_args.kwargs["model"] == "fake"
    else:
        with pytest.raises(ValueError):
            provider.generate(messages)


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Verifica configuração e criação isolada do provedor.
@pytest.mark.parametrize("judge,prefix", [(False, "LLM"), (True, "JUDGE")])
def test_factory(monkeypatch, judge, prefix):
    monkeypatch.setenv(f"{prefix}_PROVIDER", "openai")
    monkeypatch.delenv(f"{prefix}_API_KEY", raising=False)
    monkeypatch.delenv(f"{prefix}_MODEL", raising=False)
    config = ExperimentConfig()
    with pytest.raises(ValueError):
        create_provider(config, judge=judge)
    monkeypatch.setenv(f"{prefix}_API_KEY", "fake")
    monkeypatch.setenv(f"{prefix}_MODEL", "fake-model")
    client = Mock()
    monkeypatch.setattr("src.providers.factory.OpenAI", client)
    assert create_provider(config, judge=judge).model == "fake-model"
    client.assert_called_once_with(api_key="fake", max_retries=0, timeout=60)
