import pytest
from src.analytics.metrics import normalize_score, global_score, pair_score
from src.analytics.statistics import paired_bootstrap


@pytest.mark.parametrize("score,expected", [(1,0),(2,25),(3,50),(4,75),(5,100)])
def test_normalize(score, expected):
    assert normalize_score(score) == expected


def test_global():
    assert global_score(dict(clarity=5, completeness=5, corporate_tone=5,
                             safety=5, factual_grounding=5), 100) == pytest.approx(100)


def test_pair():
    assert pair_score(dict(factual_equivalence=1, decision_equivalence=1,
                           guidance_equivalence=1, safety_equivalence=1)) == 100


def test_bootstrap():
    assert paired_bootstrap({"a": 1}, {"a": 2})["ci95"] == [1, 1]
