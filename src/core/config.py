from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class ExperimentConfig(BaseModel):
    repetitions: int = Field(default=3, ge=1)
    random_seed: int = 42
    strategies: list[str] = ["P01", "P02", "P03", "P04", "P05"]
    temperature: float = Field(default=0.2, ge=0, le=2)
    top_p: float = Field(default=1.0, gt=0, le=1)
    max_output_tokens: int = Field(default=1024, gt=0)


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Carrega e valida a configuração YAML.
def load_config(root: Path) -> ExperimentConfig:
    return ExperimentConfig.model_validate(
        yaml.safe_load((root / "config/experiment_config.yaml").read_text(encoding="utf-8"))
    )
