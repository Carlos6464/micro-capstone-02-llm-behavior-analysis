from statistics import mean

WEIGHTS = {
    "clarity": 0.15,
    "completeness": 0.20,
    "corporate_tone": 0.10,
    "safety": 0.25,
    "factual_grounding": 0.15,
}


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Normaliza notas para a escala de 0 a 100.
def normalize_score(score):
    if not 1 <= score <= 5:
        raise ValueError("Nota fora da escala.")
    return (score - 1) * 25


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Calcula a equivalência ponderada.
def pair_score(pair):
    return 100 * sum(
        pair[k] * w
        for k, w in {
            "factual_equivalence": 0.4,
            "decision_equivalence": 0.3,
            "guidance_equivalence": 0.2,
            "safety_equivalence": 0.1,
        }.items()
    )


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Calcula o SGD.
def global_score(scores, consistency):
    return sum(normalize_score(scores[k]) * w for k, w in WEIGHTS.items()) + 0.15 * consistency


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Consolida indicadores por estratégia.
def aggregate(individual, pairs, planned=90, repetitions=3, responses=()):
    result = []
    for prompt in ("P01", "P02", "P03", "P04", "P05"):
        rows = [r for r in individual if r["prompt_id"] == prompt]
        groups = {}
        for r in rows:
            groups.setdefault(r["case_id"], []).append(r)
        complete = [g for g in groups.values() if len(g) == repetitions]
        pg = {}
        for p in pairs:
            if p["prompt_id"] == prompt:
                pg.setdefault(p["case_id"], []).append(pair_score(p))
        cs = [mean(v) for v in pg.values() if len(v) == repetitions * (repetitions - 1) // 2]
        scores = (
            {k: mean(mean(r["scores"][k] for r in g) for g in complete) for k in WEIGHTS}
            if complete
            else {}
        )
        consistency = mean(cs) if cs else None
        generated = [r for r in responses if r["prompt_id"] == prompt and r["status"] == "success"]
        operational = {}
        for key in ("latency_ms", "input_tokens", "output_tokens"):
            values = [r[key] for r in generated if r.get(key) is not None]
            operational[key + "_mean"] = mean(values) if values else None
        for label, records in (
            ("generation", generated),
            ("evaluation", rows + [p for p in pairs if p["prompt_id"] == prompt]),
        ):
            costs = [r.get("estimated_cost_usd") for r in records]
            operational[label + "_cost_usd"] = (
                sum(costs) if costs and all(c is not None for c in costs) else None
            )
        result.append(
            {
                "prompt_id": prompt,
                "evaluated": len(rows),
                "operational": operational,
                "review_required": sum(bool(r.get("human_review_required")) for r in rows),
                "coverage": 100 * len(rows) / planned,
                "scores": scores,
                "consistency": consistency,
                "hallucination_pct": 100 * sum(bool(r["hallucinations"]) for r in rows) / len(rows)
                if rows
                else None,
                "critical": sum(r["max_severity"] == "S4" for r in rows),
                "complete_cases": len(complete),
                "complete_pairs": len(cs),
                "sgd": global_score(scores, consistency)
                if scores and consistency is not None
                else None,
            }
        )
    return result
