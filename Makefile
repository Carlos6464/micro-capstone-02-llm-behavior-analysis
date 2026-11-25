# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Executa verificações locais sem chamadas à API e registra os resultados.
SHELL := /bin/bash
.DEFAULT_GOAL := test
.PHONY: test format

# Executa todas as verificações, mesmo quando alguma falha.
test:
	@mkdir -p logs
	@set -o pipefail; ( \
		failed=0; \
		run() { printf '\n===== %s =====\n' "$$*"; "$$@"; rc=$$?; printf 'Código de saída: %s\n' "$$rc"; if [ "$$rc" -ne 0 ]; then failed=1; fi; }; \
		printf 'Validação local — %s\n' "$$(date -Iseconds)"; \
		run git rev-parse HEAD; \
		run uv --version; \
		run git status --short; \
		run uv sync --locked; \
		run uv run python --version; \
		run uv run python -m src validate; \
		run uv run python -m src run --dry-run; \
		run uv run ruff check .; \
		run uv run ruff format --check .; \
		run uv run python -m pytest -v --cov=src --cov-report=term-missing --cov-fail-under=85; \
		printf '\nResultado geral: %s (0=sucesso, 1=falha)\n' "$$failed"; \
		exit "$$failed"; \
	) 2>&1 | tee logs/test_results.txt

# Formatação opcional: altera os arquivos Python locais.
format:
	uv run ruff format .

# Comandos explícitos de execução paga; use identificadores distintos.
.PHONY: pilot experiment evaluate report
pilot:
	@test -n "$(RUN_ID)" || (echo "Informe RUN_ID=RUN-PILOT01"; exit 1)
	uv run python -m src run --run-id "$(RUN_ID)" --cases TC-001 TC-024 TC-029 --repetitions 1 --execute

experiment:
	@test -n "$(RUN_ID)" || (echo "Informe RUN_ID=RUN-FULL01"; exit 1)
	uv run python -m src run --run-id "$(RUN_ID)" --execute

evaluate:
	@test -n "$(RUN_ID)" || (echo "Informe RUN_ID"; exit 1)
	uv run python -m src evaluate --run-id "$(RUN_ID)" --execute

report:
	@test -n "$(RUN_ID)" || (echo "Informe RUN_ID"; exit 1)
	uv run python -m src report --run-id "$(RUN_ID)"
