# Instalação e execução

Python 3.12 e uv. Execute `uv sync`, `uv run python -m src validate`, `uv run python -m src plan`, `uv run python -m src run --dry-run` e `uv run pytest`. Nenhum desses comandos chama a API. Antes de execução real, configure .env e preços verificados. Não publique credenciais. Use `run --execute` somente após autorização; `evaluate --run-id RUN_ID --execute` também gera custos. Revisão exporta fila; importação e homologação ainda pendentes. Resultados de decisão permanecem inconclusivos até revisão e rastreabilidade verificadas. Lockfile e cobertura de 85% pendentes de validação.

### Validação automatizada com Make

No Ubuntu, instale o GNU Make se necessário (`sudo apt install make`). Execute `make test` na raiz do repositório. O alvo sincroniza dependências, valida artefatos, executa dry-run, Ruff (lint e formatação) e Pytest com cobertura. Todas as verificações são executadas mesmo se alguma falhar. A saída padrão e os erros são exibidos no terminal e gravados em `logs/test_results.txt`, sobrescrito a cada execução. O comando retorna falha se qualquer verificação falhar. Não realiza chamadas pagas à API. Envie esse arquivo para análise, após verificar se não contém informações sensíveis. `make format` é opcional e modifica os arquivos locais; `make test` não formata o código.

### Validação ampliada — 25/11/2026

Baseline local informado: 12 testes aprovados, cobertura de 27%, lint e formatação aprovados, zero chamadas pagas. O lockfile publicado pelo responsável foi preservado. Novos testes unitários e de integração usam mocks para geração e avaliação, incluindo retomada, decisão, ranking, CLI e relatórios. Makefile e CI exigem cobertura de 85% e sincronização com lockfile. A nova suíte ainda precisa ser executada; não há confirmação de cobertura ou homologação. Use `make test` e consulte `logs/test_results.txt`.
