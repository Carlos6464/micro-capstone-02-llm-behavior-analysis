from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter

from src.core.schemas import BenchmarkInput, ExperimentTask
from src.infrastructure.cost_tracker import CostTracker
from src.infrastructure.hashing import sha256
from src.infrastructure.storage import append_record, read_records
from src.prompting.prompt_builder import build_messages
from src.providers.base import LLMProvider


class ExperimentRunner:
    # Autor: Carlos Adriano
    # Data: 25/11/2026
    # Descrição: Inicializa as dependências do componente.
    def __init__(
        self, provider: LLMProvider, storage: Path, budget: CostTracker, max_output_tokens: int
    ):
        self.provider = provider
        self.storage = storage
        self.budget = budget
        self.max_output_tokens = max_output_tokens

    # Autor: Carlos Adriano
    # Data: 25/11/2026
    # Descrição: Executa tarefas pendentes e registra respostas e custos.
    def run(
        self,
        tasks: list[ExperimentTask],
        cases: list[BenchmarkInput],
        prompts: dict[str, str],
        knowledge: str,
    ) -> None:
        by_id = {case.case_id: case for case in cases}
        path = self.storage / "responses.jsonl"
        existing = read_records(path)
        completed = {row["execution_id"] for row in existing if row["status"] == "success"}
        attempts = read_records(self.storage / "attempts.jsonl")
        latest = {row["execution_id"]: row for row in attempts}
        if any(row.get("status") != "success" for row in latest.values()):
            raise RuntimeError("Tentativas com cobrança incerta exigem reconciliação manual.")
        self.budget.spent = sum(
            row["estimated_cost_usd"] for row in existing if row["status"] == "success"
        )
        for task in tasks:
            if task.execution_id in completed:
                continue
            messages = build_messages(prompts[task.prompt_id], knowledge, by_id[task.case_id])
            estimated_input = sum(len(m.content.encode("utf-8")) for m in messages) + 128
            self.budget.check(estimated_input, self.max_output_tokens)
            start = perf_counter()
            base = dict(
                task.model_dump(),
                execution_id=task.execution_id,
                prompt_hash=sha256(prompts[task.prompt_id]),
                knowledge_base_hash=sha256(knowledge),
                executed_at=datetime.now(UTC).isoformat(),
            )
            append_record(self.storage / "attempts.jsonl", dict(base, status="started"))
            try:
                response = self.provider.generate(messages)
                cost = self.budget.record(response.input_tokens, response.output_tokens)
            except Exception as error:
                append_record(path, dict(base, status="failed", error_type=type(error).__name__))
                raise
            append_record(
                path,
                dict(
                    base,
                    status="success",
                    response_text=response.text,
                    model=response.model,
                    request_id=response.request_id,
                    input_tokens=response.input_tokens,
                    output_tokens=response.output_tokens,
                    latency_ms=(perf_counter() - start) * 1000,
                    estimated_cost_usd=cost,
                ),
            )
            append_record(self.storage / "attempts.jsonl", dict(base, status="success"))
