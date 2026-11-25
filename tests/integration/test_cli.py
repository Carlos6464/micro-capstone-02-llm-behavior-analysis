import sys

import pytest

from src.cli import main


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Exercita comandos locais e bloqueio de execução sem autorização.
@pytest.mark.parametrize(
    "args,expected",
    [
        (["validate"], "450 tarefas"),
        (["plan"], "TC-"),
        (["estimate"], '"paid_calls": 0'),
        (["run", "--dry-run"], '"paid_calls": 0'),
        (["run", "--dry-run", "--cases", "TC-001", "--repetitions", "1"], '"generation_calls": 5'),
    ],
)
def test_cli(monkeypatch, capsys, args, expected):
    monkeypatch.setattr(sys, "argv", ["src", *args])
    main()
    assert expected in capsys.readouterr().out


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Confirma que execução real exige autorização explícita.
def test_cli_guard(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["src", "run"])
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 2


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Exercita relatório e revisão de piloto sem chamadas externas.
def test_pilot_report_cli(tmp_path, monkeypatch):
    import json
    import shutil
    import sys
    from pathlib import Path

    from src.cli import main

    root = Path(__file__).resolve().parents[2]
    for name in ("config", "data", "prompts"):
        shutil.copytree(root / name, tmp_path / name)
    raw = tmp_path / "results/raw/RUN-TEST"
    evaluated = tmp_path / "results/evaluated/RUN-TEST"
    raw.mkdir(parents=True)
    evaluated.mkdir(parents=True)
    identifier = "TC-001-P01-1"
    response = {
        "execution_id": identifier,
        "prompt_id": "P01",
        "status": "success",
        "response_text": "Verifique a conexão.",
    }
    record = {
        "execution_id": identifier,
        "case_id": "TC-001",
        "prompt_id": "P01",
        "category": "tech",
        "scores": dict.fromkeys(
            ("clarity", "completeness", "corporate_tone", "safety", "factual_grounding"), 5
        ),
        "evidence": ["Verifique a conexão."],
        "hallucinations": [],
        "max_severity": "S0",
        "human_review_required": False,
    }
    (raw / "responses.jsonl").write_text(json.dumps(response) + "\n")
    (evaluated / "individual_evaluations.jsonl").write_text(json.dumps(record) + "\n")
    manifest = {"config": {"repetitions": 1}, "tasks": [{}] * 5}
    (raw / "run_manifest.json").write_text(json.dumps(manifest))
    for command in ("status", "review", "report", "analyze"):
        monkeypatch.setattr(
            sys,
            "argv",
            ["src", command, "--root", str(tmp_path), "--run-id", "RUN-TEST"],
        )
        main()
    report = tmp_path / "results/reports/RUN-TEST"
    assert (report / "individual_scores.png").exists()
    rows = json.loads((report / "decision_summary.json").read_text())
    assert rows[0]["coverage"] == 100
    assert rows[0]["sgd"] is None
    assert (evaluated / "human_review_queue.json").exists()
    assert (evaluated / "audited_evaluations.json").exists()
