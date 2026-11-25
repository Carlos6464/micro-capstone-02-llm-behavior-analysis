import random

from src.core.config import ExperimentConfig
from src.core.schemas import BenchmarkInput, ExperimentTask


def plan(cases: list[BenchmarkInput], config: ExperimentConfig) -> list[ExperimentTask]:
    tasks = [ExperimentTask(case_id=case.case_id, prompt_id=prompt, repetition=rep)
             for case in cases for prompt in config.strategies
             for rep in range(1, config.repetitions + 1)]
    if len({task.execution_id for task in tasks}) != len(tasks):
        raise ValueError("Tarefas duplicadas.")
    random.Random(config.random_seed).shuffle(tasks)
    return tasks
