import argparse
import json
import os
from pathlib import Path
from uuid import uuid4

import yaml
from dotenv import load_dotenv

from src.core.config import load_config
from src.data.dataset_loader import load_expectations, load_inputs
from src.data.knowledge_loader import load_knowledge
from src.experiments.experiment_plan import plan
from src.infrastructure.hashing import sha256
from src.infrastructure.storage import append_record, read_records
from src.prompting.prompt_builder import build_messages
from src.prompting.prompt_registry import load_prompts


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Orquestra os comandos da aplicação.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=[
            "validate",
            "plan",
            "estimate",
            "run",
            "evaluate",
            "review",
            "analyze",
            "report",
            "status",
        ],
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--run-id")
    parser.add_argument("--resume")
    parser.add_argument("--confirm-legacy-503", action="store_true")
    parser.add_argument("--cases", nargs="+")
    parser.add_argument("--repetitions", type=int)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("--import-reviews", type=Path)
    args = parser.parse_args()
    root = args.root
    cases = load_inputs(root)
    expectations = load_expectations(root)
    if sorted(c.case_id for c in cases) != sorted(e.case_id for e in expectations):
        raise ValueError("Referências incompatíveis.")
    knowledge, prompts, config = load_knowledge(root), load_prompts(root), load_config(root)
    for c in cases:
        for template in prompts.values():
            build_messages(template, knowledge, c)
    if args.cases:
        cases = [c for c in cases if c.case_id in args.cases]
        if len(cases) != len(set(args.cases)):
            raise ValueError("Casos desconhecidos.")
    if args.repetitions is not None:
        config = type(config).model_validate(
            dict(config.model_dump(), repetitions=args.repetitions)
        )
    tasks = plan(cases, config)
    if args.command == "validate":
        print(f"{len(cases)} casos; {len(prompts)} prompts; {len(tasks)} tarefas.")
        return
    if args.command == "plan":
        print(json.dumps([t.model_dump() for t in tasks], ensure_ascii=False))
        return
    if args.command == "estimate" or (args.command == "run" and args.dry_run):
        print(
            json.dumps(
                {
                    "generation_calls": len(tasks),
                    "individual_calls": len(tasks),
                    "pair_calls": len(cases)
                    * len(prompts)
                    * config.repetitions
                    * (config.repetitions - 1)
                    // 2,
                    "paid_calls": 0,
                }
            )
        )
        return
    run_id = args.resume or args.run_id or ("RUN-" + uuid4().hex)
    if not run_id.startswith("RUN-") or not run_id[4:].isalnum():
        raise ValueError("Identificador inválido.")
    raw = root / "results/raw" / run_id
    evaluated = root / "results/evaluated" / run_id
    if args.command in ("run", "evaluate"):
        if not args.execute:
            parser.error("Chamadas reais exigem --execute.")
        load_dotenv(root / ".env")
        from src.infrastructure.cost_tracker import CostTracker
        from src.providers.factory import create_provider

        pricing = yaml.safe_load((root / "config/pricing_config.yaml").read_text())
        prefix = "LLM" if args.command == "run" else "JUDGE"
        provider_name = os.environ.get(f"{prefix}_PROVIDER", "openai").lower()
        if provider_name == "gemini":
            if os.environ.get(f"{prefix}_MODEL") != "gemini-2.5-flash":
                raise ValueError("Modelo Gemini sem preço configurado.")
            section = pricing["gemini-2.5-flash"]
        elif provider_name == "openai":
            section = pricing["generation" if args.command == "run" else "judge"]
        else:
            raise ValueError("Provedor desconhecido.")
        limit = float(os.environ["MAX_COST_USD"])
        budget = CostTracker(
            limit, float(section["input_usd_per_million"]), float(section["output_usd_per_million"])
        )
        if args.command == "run":
            from src.experiments.experiment_runner import ExperimentRunner

            manifest = {
                "tasks": [t.model_dump() for t in tasks],
                "config": config.model_dump(),
                "model": os.environ.get("LLM_MODEL"),
                "provider": provider_name,
                "knowledge_hash": sha256(knowledge),
                "prompt_hash": sha256(json.dumps(prompts, sort_keys=True)),
                "dataset_hash": sha256(json.dumps([c.model_dump() for c in cases])),
            }
            raw.mkdir(parents=True, exist_ok=True)
            path = raw / "run_manifest.json"
            if path.exists() and json.loads(path.read_text()) != manifest:
                raise ValueError("Manifesto divergente; use configuração original.")
            path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
            if args.confirm_legacy_503:
                journal = raw / "attempts.jsonl"
                latest = {r["execution_id"]: r for r in read_records(journal)}
                pending = [r for r in latest.values() if r["status"] == "started"]
                failures = read_records(raw / "responses.jsonl")
                if len(pending) != 1 or not failures:
                    raise ValueError("Não há uma única tentativa legada para reconciliar.")
                last = failures[-1]
                if (
                    last["execution_id"] != pending[0]["execution_id"]
                    or last["status"] != "failed"
                    or last.get("error_type") != "HTTPError"
                ):
                    raise ValueError("Falha legada incompatível com confirmação de HTTP 503.")
                append_record(journal, dict(pending[0], status="retryable_503"))
            ExperimentRunner(create_provider(config), raw, budget, config.max_output_tokens).run(
                tasks, cases, prompts, knowledge
            )
        else:
            from src.evaluation.evaluation_runner import evaluate

            if not raw.exists():
                raise ValueError("Execução inexistente.")
            budget.spent = sum(
                r.get("estimated_cost_usd", 0)
                for p in (
                    raw / "responses.jsonl",
                    evaluated / "individual_evaluations.jsonl",
                    evaluated / "consistency_evaluations.jsonl",
                )
                for r in read_records(p)
            )
            evaluate(
                root,
                raw,
                evaluated,
                cases,
                expectations,
                knowledge,
                create_provider(config, judge=True),
                budget,
                config.max_output_tokens,
            )
        print(run_id)
        return
    if not raw.exists():
        raise ValueError("Execução inexistente; informe --run-id.")
    from src.evaluation.deterministic_evaluator import audit_record

    responses = read_records(raw / "responses.jsonl")
    originals = read_records(evaluated / "individual_evaluations.jsonl")
    by_id = {r["execution_id"]: r for r in responses if r["status"] == "success"}
    individual = [audit_record(r, by_id[r["execution_id"]]) for r in originals]
    pairs = read_records(evaluated / "consistency_evaluations.jsonl")
    if args.command == "status":
        print(
            json.dumps(
                {
                    "run_id": run_id,
                    "responses": len(read_records(raw / "responses.jsonl")),
                    "evaluations": len(individual),
                    "pairs": len(pairs),
                }
            )
        )
    elif args.command == "review":
        from src.evaluation.human_review import review_queue, validate_reviews

        evaluated.mkdir(parents=True, exist_ok=True)
        if args.import_reviews:
            reviews = validate_reviews(
                json.loads(args.import_reviews.read_text(encoding="utf-8")), individual
            )
            target = evaluated / "human_review_results.json"
            if target.exists():
                raise ValueError("Revisões já importadas; preserve o arquivo original.")
            target.write_text(json.dumps(reviews, ensure_ascii=False, indent=2), encoding="utf-8")
        (evaluated / "human_review_queue.json").write_text(
            json.dumps(review_queue(individual), ensure_ascii=False, indent=2), encoding="utf-8"
        )
    else:
        from src.analytics.decision_engine import decide
        from src.analytics.metrics import aggregate

        manifest = json.loads((raw / "run_manifest.json").read_text(encoding="utf-8"))
        repetitions = manifest["config"]["repetitions"]
        planned = len(manifest["tasks"]) // len(prompts)
        rows = aggregate(individual, pairs, planned, repetitions, responses)
        evaluated.mkdir(parents=True, exist_ok=True)
        (evaluated / "audited_evaluations.json").write_text(
            json.dumps(individual, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        for row in rows:
            row["decision"] = decide(row)
            row["scope"] = "full" if planned == 90 and repetitions == 3 else "pilot"
        if args.command == "report":
            from src.reporting.report_generator import report

            report(rows, root / "results/reports" / run_id)
        else:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
