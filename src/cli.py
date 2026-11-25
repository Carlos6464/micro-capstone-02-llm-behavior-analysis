import argparse
import json
from pathlib import Path

from src.core.config import load_config
from src.data.dataset_loader import load_expectations, load_inputs
from src.data.knowledge_loader import load_knowledge
from src.experiments.experiment_plan import plan
from src.prompting.prompt_builder import build_messages
from src.prompting.prompt_registry import load_prompts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["validate", "plan"])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    cases = load_inputs(args.root)
    expectations = load_expectations(args.root)
    if sorted(c.case_id for c in cases) != sorted(e.case_id for e in expectations):
        raise ValueError("Referências de avaliação incompatíveis.")
    knowledge = load_knowledge(args.root)
    prompts = load_prompts(args.root)
    config = load_config(args.root)
    tasks = plan(cases, config)
    for case in cases:
        for template in prompts.values():
            build_messages(template, knowledge, case)
    if args.command == "plan":
        print(json.dumps([task.model_dump() for task in tasks], ensure_ascii=False))
    else:
        print(f"{len(cases)} casos; {len(prompts)} prompts; {len(tasks)} tarefas planejadas.")
