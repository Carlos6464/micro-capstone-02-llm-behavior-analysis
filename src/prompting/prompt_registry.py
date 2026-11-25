from pathlib import Path

import yaml


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Carrega os cinco templates aprovados.
def load_prompts(root: Path) -> dict[str, str]:
    directory = root / "prompts"
    registry = yaml.safe_load((directory / "prompt_registry.yaml").read_text(encoding="utf-8"))
    rows = registry["prompts"]
    result = {
        row["prompt_id"]: (directory / row["template"]).read_text(encoding="utf-8")
        for row in rows
        if row["status"] == "approved"
    }
    if set(result) != {"P01", "P02", "P03", "P04", "P05"}:
        raise ValueError("Registro de estratégias inválido.")
    return result
