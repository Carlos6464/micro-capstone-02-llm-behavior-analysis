from pathlib import Path

from src.core.config import load_config
from src.data.dataset_loader import load_inputs
from src.data.knowledge_loader import load_knowledge
from src.experiments.experiment_plan import plan
from src.prompting.prompt_builder import build_messages
from src.prompting.prompt_registry import load_prompts

ROOT = Path(__file__).resolve().parents[2]


def test_plan():
    tasks = plan(load_inputs(ROOT), load_config(ROOT))
    assert len(tasks) == len({t.execution_id for t in tasks}) == 450


def test_messages():
    case = load_inputs(ROOT)[0]
    for template in load_prompts(ROOT).values():
        messages = build_messages(template, load_knowledge(ROOT), case)
        assert [m.role for m in messages] == ["system", "user"]
        assert messages[1].content == case.customer_query
