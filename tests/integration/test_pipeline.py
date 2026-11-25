import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from src.analytics.metrics import aggregate
from src.core.schemas import ExperimentTask
from src.data.dataset_loader import load_expectations, load_inputs
from src.data.knowledge_loader import load_knowledge
from src.evaluation.evaluation_runner import evaluate
from src.evaluation.human_review import review_queue
from src.experiments.experiment_runner import ExperimentRunner
from src.infrastructure.cost_tracker import CostTracker
from src.infrastructure.storage import read_records
from src.prompting.prompt_registry import load_prompts
from src.providers.base import ProviderResponse
from src.reporting.report_generator import report

ROOT = Path(__file__).resolve().parents[2]


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Exercita geração, retomada, avaliação, agregação e relatório com mocks.
def test_pipeline(tmp_path):
    cases = load_inputs(ROOT)[:1]
    expectations = load_expectations(ROOT)
    knowledge = load_knowledge(ROOT)
    prompts = load_prompts(ROOT)
    tasks = [
        ExperimentTask(case_id=cases[0].case_id, prompt_id="P01", repetition=i)
        for i in range(1, 4)
    ]
    provider = Mock()
    provider.generate.return_value = ProviderResponse("Resposta simulada", "fake", 10, 5)
    raw = tmp_path / "raw"
    runner = ExperimentRunner(provider, raw, CostTracker(100, 1, 1), 100)
    runner.run(tasks, cases, prompts, knowledge)
    runner.run(tasks, cases, prompts, knowledge)
    assert provider.generate.call_count == 3
    assert len(read_records(raw / "responses.jsonl")) == 3
    scores = dict.fromkeys(
        ["clarity", "completeness", "corporate_tone", "safety", "factual_grounding"], 5
    )
    judgment = {
        "scores": scores,
        "expected_facts": [],
        "hallucinations": [],
        "security_violations": [],
        "max_severity": "S0",
        "evidence": ["simulado"],
        "human_review_required": True,
    }
    pair = {
        "factual_equivalence": 1,
        "decision_equivalence": 1,
        "guidance_equivalence": 1,
        "safety_equivalence": 1,
        "critical_contradiction": False,
        "evidence": ["simulado"],
        "human_review_required": False,
    }
    judge = Mock()
    judge.generate.side_effect = [
        ProviderResponse(json.dumps(value), "fake", 10, 5)
        for value in [judgment] * 3 + [pair] * 3
    ]
    output = tmp_path / "evaluated"
    budget = CostTracker(100, 1, 1)
    evaluate(ROOT, raw, output, cases, expectations, knowledge, judge, budget, 100)
    evaluate(ROOT, raw, output, cases, expectations, knowledge, judge, budget, 100)
    assert judge.generate.call_count == 6
    individual = read_records(output / "individual_evaluations.jsonl")
    pairs = read_records(output / "consistency_evaluations.jsonl")
    assert len(review_queue(individual)) == 3
    rows = aggregate(individual, pairs, planned=3)
    assert rows[0]["sgd"] == pytest.approx(100)
    assert rows[0]["coverage"] == 100
    report(rows, tmp_path / "report")
    assert (tmp_path / "report/sgd.png").is_file()
    assert (tmp_path / "report/strategy_metrics.csv").is_file()


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Impede repetição de chamadas após falha de cobrança incerta.
def test_failed_run(tmp_path):
    cases = load_inputs(ROOT)[:1]
    tasks = [ExperimentTask(case_id=cases[0].case_id, prompt_id="P01", repetition=1)]
    provider = Mock()
    provider.generate.side_effect = RuntimeError("falha simulada")
    runner = ExperimentRunner(provider, tmp_path, CostTracker(100, 1, 1), 100)
    prompts, knowledge = load_prompts(ROOT), load_knowledge(ROOT)
    with pytest.raises(RuntimeError, match="falha simulada"):
        runner.run(tasks, cases, prompts, knowledge)
    assert read_records(tmp_path / "responses.jsonl")[0]["status"] == "failed"
    with pytest.raises(RuntimeError, match="reconciliação"):
        runner.run(tasks, cases, prompts, knowledge)
    assert provider.generate.call_count == 1
