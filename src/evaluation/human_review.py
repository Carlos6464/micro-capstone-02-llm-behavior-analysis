import math
import random
from collections import defaultdict


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Seleciona registros para revisão humana obrigatória e amostral.
def review_queue(records, seed=42):
    required = [r for r in records if r["human_review_required"]]
    strata = defaultdict(list)
    for r in records:
        if not r["human_review_required"]:
            strata[r["prompt_id"], r["category"]].append(r)
    rng = random.Random(seed)
    for key in sorted(strata):
        group = sorted(strata[key], key=lambda r: r["execution_id"])
        required.extend(rng.sample(group, math.ceil(len(group) * 0.2)))
    return required


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Valida decisões humanas sem sobrescrever avaliações originais.
def validate_reviews(reviews, records):
    known = {r["execution_id"] for r in records}
    seen = set()
    for review in reviews:
        identifier = review["execution_id"]
        if identifier not in known or identifier in seen:
            raise ValueError("Identificador de revisão inválido ou duplicado.")
        if review.get("decision") not in ("confirmed", "rejected", "corrected"):
            raise ValueError("Decisão de revisão inválida.")
        if not str(review.get("reviewer", "")).strip() or not str(review.get("notes", "")).strip():
            raise ValueError("Informe revisor e justificativa.")
        seen.add(identifier)
    return reviews
