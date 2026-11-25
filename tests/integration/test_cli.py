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
