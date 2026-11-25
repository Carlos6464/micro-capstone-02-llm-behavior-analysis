import os

from openai import OpenAI

from src.core.config import ExperimentConfig
from src.providers.openai_provider import OpenAIProvider


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Instancia o adaptador com configuração do ambiente.
def create_provider(config: ExperimentConfig, *, judge: bool = False):
    prefix = "JUDGE" if judge else "LLM"
    key = os.environ.get(f"{prefix}_API_KEY")
    model = os.environ.get(f"{prefix}_MODEL")
    if not key or not model:
        raise ValueError(f"Configure {prefix}_API_KEY e {prefix}_MODEL.")
    client = OpenAI(api_key=key, max_retries=0, timeout=60)
    return OpenAIProvider(client, model, config.temperature, config.top_p,
                          config.max_output_tokens)
