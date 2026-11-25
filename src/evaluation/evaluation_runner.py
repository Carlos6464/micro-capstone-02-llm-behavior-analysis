import json
from itertools import combinations
from pathlib import Path

from pydantic import BaseModel, Field
from typing import Literal

from src.core.schemas import LLMMessage
from src.infrastructure.storage import append_record, read_records


class Scores(BaseModel):
    clarity: int = Field(ge=1, le=5, strict=True)
    completeness: int = Field(ge=1, le=5, strict=True)
    corporate_tone: int = Field(ge=1, le=5, strict=True)
    safety: int = Field(ge=1, le=5, strict=True)
    factual_grounding: int = Field(ge=1, le=5, strict=True)


class Judgment(BaseModel):
    scores: Scores
    expected_facts: list[dict]
    hallucinations: list[dict]
    security_violations: list[dict]
    max_severity: Literal["S0", "S1", "S2", "S3", "S4"]
    evidence: list[str]
    human_review_required: bool


class PairJudgment(BaseModel):
    factual_equivalence: Literal[0, 0.5, 1]
    decision_equivalence: Literal[0, 0.5, 1]
    guidance_equivalence: Literal[0, 0.5, 1]
    safety_equivalence: Literal[0, 0.5, 1]
    critical_contradiction: bool
    evidence: list[str]
    human_review_required: bool


def evaluate(root, raw, output, cases, expectations, knowledge, provider, budget, max_tokens):
    rubrics = "\n".join((root / "docs/methodology" / name).read_text(encoding="utf-8")
                        for name in ("evaluation_rubrics.md", "hallucination_taxonomy.md",
                                     "security_violation_taxonomy.md"))
    case_map = {c.case_id: c for c in cases}
    expected = {e.case_id: e for e in expectations}
    rows = [r for r in read_records(raw / "responses.jsonl") if r["status"] == "success"]
    def judge(template, schema, values):
        system = (root / "prompts" / template).read_text(encoding="utf-8")
        # Keep untrusted content in a separate user message.
        system = system.split("RUBRICAS:")[0] + "\n" + rubrics + "\n" + knowledge
        system += "\nSchema JSON: " + json.dumps(schema.model_json_schema(), ensure_ascii=False)
        user = json.dumps(values, ensure_ascii=False)
        budget.check(len((system + user).encode("utf-8")) + 128, max_tokens)
        result = provider.generate([LLMMessage(role="system", content=system),
                                    LLMMessage(role="user", content=user)])
        cost = budget.record(result.input_tokens, result.output_tokens)
        return schema.model_validate_json(result.text), cost
    individual = output / "individual_evaluations.jsonl"
    pairs = output / "consistency_evaluations.jsonl"
    done = {r["execution_id"] for r in read_records(individual)}
    for row in rows:
        if row["execution_id"] in done:
            continue
        c = case_map[row["case_id"]]
        e = expected[c.case_id]
        result, cost = judge("evaluation_judge.txt", Judgment, {
            "channel": c.channel, "customer_query": c.customer_query,
            "model_response": row["response_text"], "expected_behavior": e.expected_behavior,
            "expected_facts": e.expected_facts, "forbidden_behavior": e.forbidden_behavior,
            "knowledge_references": e.knowledge_references})
        record = result.model_dump()
        if result.max_severity == "S4":
            record["scores"]["safety"] = 1
        append_record(individual, dict(record, execution_id=row["execution_id"],
                      case_id=c.case_id, prompt_id=row["prompt_id"], repetition=row["repetition"],
                      category=e.category, risk_level=e.risk_level, estimated_cost_usd=cost,
                      human_review_required=result.human_review_required or e.risk_level == "critical"
                      or result.max_severity == "S4"))
    done_pairs = {r["pair_id"] for r in read_records(pairs)}
    groups = {}
    for row in rows:
        groups.setdefault((row["case_id"], row["prompt_id"]), []).append(row)
    for (case_id, prompt_id), group in groups.items():
        for a, b in combinations(sorted(group, key=lambda r: r["repetition"]), 2):
            pair_id = a["execution_id"] + ":" + b["execution_id"]
            if pair_id in done_pairs:
                continue
            c = case_map[case_id]
            result, cost = judge("consistency_judge.txt", PairJudgment, {
                "customer_query": c.customer_query, "channel": c.channel,
                "response_a": a["response_text"], "response_b": b["response_text"]})
            append_record(pairs, dict(result.model_dump(), pair_id=pair_id, case_id=case_id,
                          prompt_id=prompt_id, estimated_cost_usd=cost))
