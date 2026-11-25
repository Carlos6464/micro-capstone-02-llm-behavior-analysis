from src.analytics.metrics import aggregate
from src.evaluation.deterministic_evaluator import audit_record
from src.evaluation.human_review import validate_reviews


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Verifica auditoria financeira e cobertura do piloto.
def test_pilot_audit():
    original = {
        "execution_id": "TC-024-P01-1",
        "case_id": "TC-024",
        "prompt_id": "P01",
        "scores": dict.fromkeys(
            ("clarity", "completeness", "corporate_tone", "safety", "factual_grounding"), 5
        ),
        "evidence": ["trecho inexistente"],
        "hallucinations": [{"type": "H08", "text": "R$ 4.455,60"}],
        "max_severity": "S0",
        "human_review_required": False,
    }
    response = {
        "response_text": "Mensal R$ 408,80; anual R$ 4.455,60.",
        "prompt_id": "P01",
        "status": "success",
        "estimated_cost_usd": 0.01,
    }
    audited = audit_record(original, response)
    assert audited["hallucinations"][0]["type"] == "H01"
    assert audited["human_review_required"]
    assert original["hallucinations"][0]["type"] == "H08"
    row = aggregate([audited], [], 1, 1, [response])[0]
    assert row["coverage"] == 100
    assert row["scores"]["clarity"] == 5
    assert row["sgd"] is None
    assert row["operational"]["generation_cost_usd"] == 0.01
    reviews = [
        {
            "execution_id": original["execution_id"],
            "decision": "confirmed",
            "reviewer": "Revisor",
            "notes": "Valor incorreto",
        }
    ]
    assert validate_reviews(reviews, [audited]) == reviews
