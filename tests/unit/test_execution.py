from src.infrastructure.cost_tracker import CostTracker
from src.infrastructure.storage import append_record, read_records

import pytest


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Verifica cálculo e bloqueio de orçamento.
def test_cost():
    tracker = CostTracker(1, 1, 2)
    assert tracker.record(1000, 500) == pytest.approx(0.002)
    with pytest.raises(RuntimeError):
        tracker.check(1000000, 1000000)


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Verifica gravação e leitura de registros.
def test_storage(tmp_path):
    path = tmp_path / "records.jsonl"
    append_record(path, {"text": "Olá"})
    append_record(path, {"text": "Mundo"})
    assert read_records(path) == [{"text": "Olá"}, {"text": "Mundo"}]
