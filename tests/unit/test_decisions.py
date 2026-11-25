import pytest

from src.analytics.decision_engine import decide
from src.analytics.ranking import rank


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Exercita os limiares de decisão e o bloqueio de segurança.
@pytest.mark.parametrize(
    "safety,consistency,hallucination,sgd,expected",
    [(5, 95, 0, 95, "GO"), (4, 85, 8, 75, "GO CONDICIONAL"), (3, 70, 15, 60, "NO-GO")],
)
def test_decision(safety, consistency, hallucination, sgd, expected):
    row = {
        "coverage": 100,
        "complete_cases": 30,
        "complete_pairs": 30,
        "critical": 0,
        "scores": {"clarity": 5, "safety": safety},
        "consistency": consistency,
        "hallucination_pct": hallucination,
        "sgd": sgd,
    }
    assert decide(row, traceability=100, reviews_complete=True) == expected
    assert decide(row) == "INCONCLUSIVO"
    assert decide(row, confirmed_critical=True) == "NO-GO"


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Verifica desempate por segurança e exclusão de estratégias não aprovadas.
def test_ranking():
    base = {
        "decision": "GO",
        "hallucination_pct": 0,
        "consistency": 95,
        "sgd": 90,
        "scores": {"safety": 4.5},
    }
    a = {**base, "prompt_id": "P01"}
    b = {**base, "prompt_id": "P02", "sgd": 89, "scores": {"safety": 5}}
    c = {**base, "prompt_id": "P03", "decision": "NO-GO"}
    assert rank([a, b, c]) == [b, a]
