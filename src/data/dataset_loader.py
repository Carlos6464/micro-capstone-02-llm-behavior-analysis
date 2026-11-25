import json
from pathlib import Path

from src.core.schemas import BenchmarkExpectation, BenchmarkInput


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Carrega e valida entradas experimentais.
def load_inputs(root: Path) -> list[BenchmarkInput]:
    path = root / "data/processed/benchmark_inputs.jsonl"
    rows = [
        BenchmarkInput.model_validate(json.loads(line))
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(rows) < 15 or len({row.case_id for row in rows}) != len(rows):
        raise ValueError("Dataset insuficiente ou IDs duplicados.")
    return rows


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Carrega referências de avaliação.
def load_expectations(root: Path) -> list[BenchmarkExpectation]:
    path = root / "data/processed/benchmark_expectations.jsonl"
    return [
        BenchmarkExpectation.model_validate(json.loads(line))
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
