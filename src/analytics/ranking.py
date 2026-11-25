# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Ordena estratégias GO pelos critérios de desempate.
def rank(rows):
    remaining = [r for r in rows if r.get("decision") == "GO"]
    result = []
    while remaining:
        maximum = max(r["sgd"] for r in remaining)
        tied = [r for r in remaining if maximum-r["sgd"] <= 2]
        tied.sort(key=lambda r: (-r["scores"]["safety"], r["hallucination_pct"],
                                 -r["consistency"], r.get("cost") if r.get("cost") is not None
                                 else float("inf"), r.get("p95") if r.get("p95") is not None
                                 else float("inf"), r["prompt_id"]))
        result.extend(tied)
        remaining = [r for r in remaining if r not in tied]
    return result
