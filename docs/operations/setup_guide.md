# Instalação e execução

Python 3.12 e uv. Execute `uv sync`, `uv run python -m src validate`, `uv run python -m src plan`, `uv run python -m src run --dry-run` e `uv run pytest`. Nenhum desses comandos chama a API. Antes de execução real, configure .env e preços verificados. Não publique credenciais. Use `run --execute` somente após autorização; `evaluate --run-id RUN_ID --execute` também gera custos. Revisão exporta fila; importação e homologação ainda pendentes. Resultados de decisão permanecem inconclusivos até revisão e rastreabilidade verificadas. Lockfile e cobertura de 85% pendentes de validação.

### Validação automatizada com Make

No Ubuntu, instale o GNU Make se necessário (`sudo apt install make`). Execute `make test` na raiz do repositório. O alvo sincroniza dependências, valida artefatos, executa dry-run, Ruff (lint e formatação) e Pytest com cobertura. Todas as verificações são executadas mesmo se alguma falhar. A saída padrão e os erros são exibidos no terminal e gravados em `logs/test_results.txt`, sobrescrito a cada execução. O comando retorna falha se qualquer verificação falhar. Não realiza chamadas pagas à API. Envie esse arquivo para análise, após verificar se não contém informações sensíveis. `make format` é opcional e modifica os arquivos locais; `make test` não formata o código.

### Validação ampliada — 25/11/2026

Baseline local informado: 12 testes aprovados, cobertura de 27%, lint e formatação aprovados, zero chamadas pagas. O lockfile publicado pelo responsável foi preservado. Novos testes unitários e de integração usam mocks para geração e avaliação, incluindo retomada, decisão, ranking, CLI e relatórios. Makefile e CI exigem cobertura de 85% e sincronização com lockfile. A nova suíte ainda precisa ser executada; não há confirmação de cobertura ou homologação. Use `make test` e consulte `logs/test_results.txt`.

## Integração Gemini — Google AI Studio

O adaptador usa a API REST oficial generateContent via biblioteca padrão Python, evitando alterar o uv.lock. A fábrica seleciona Gemini ou OpenAI pelas variáveis LLM_PROVIDER e JUDGE_PROVIDER. Modelo Gemini homologável: gemini-2.5-flash. Temperatura de geração 0,2 e julgamento 0,0; thinkingBudget=0, JSON no julgamento, sem ferramentas e sem retries automáticos. O mesmo modelo como juiz é uma limitação metodológica. Preços de referência: USD 0,30 entrada e 2,50 saída por milhão de tokens (https://ai.google.dev/gemini-api/docs/pricing). Orçamento estimado, não teto garantido; cobranças de falhas podem não ser contabilizadas. Não publique .env.

Copie .env.example para .env sem sobrescrever configuração existente e preencha ambas as chaves. Execute make test antes de qualquer chamada. Após validação e autorização de gasto, make pilot RUN_ID=RUN-PILOT01 gera 15 respostas, make evaluate RUN_ID=RUN-PILOT01 avalia 15 respostas, e make report RUN_ID=RUN-PILOT01 produz relatório parcial (inconclusivo). O experimento completo usa make experiment RUN_ID=RUN-FULL01 e avaliação separada; não iniciar antes de homologação. Não reutilize identificadores entre piloto e experimento completo. A integração REST ainda não foi validada em rede. A avaliação determinística, revisão humana importada e rastreabilidade integral permanecem pendentes.

## Correções pós-piloto

Relatórios usam o manifesto para cobertura e repetições. Sem pares, SGD permanece indisponível e o gráfico individual é produzido. Métricas operacionais incluem médias de latência e tokens de geração e custos por fase. Auditoria local preserva JSONL originais, exporta audited_evaluations.json e sinaliza evidências não literais e valores suspeitos do TC-024 (H01). Regra específica, não verificador financeiro universal; flags exigem revisão. Notas originais não são alteradas automaticamente. Importação humana: `uv run python -m src review --run-id RUN-PILOT01 --import-reviews reviews.json`; JSON com lista de execution_id, decision (confirmed/rejected/corrected), reviewer e notes. Importação ainda não aplica correções às notas nem libera GO. Execute `make report RUN_ID=RUN-PILOT01` para reprocessar sem API e `uv run python -m src review --run-id RUN-PILOT01 --export` para fila. Testes novos pendentes de execução local.

### Retomada após HTTP 503

Gemini tenta novamente HTTP 503 até três chamadas, com esperas de 15 e 30 segundos. Se persistir, registra estado retryable_503 e permite retomar o mesmo manifesto, preservando sucessos. Para falha anterior a esta versão, somente quando o terminal comprovou HTTP 503: `uv run python -m src run --resume RUN-FULL01 --execute --confirm-legacy-503`. A confirmação é manual pois o registro antigo não guardava o código HTTP. Outros erros de cobrança incerta continuam bloqueados. Repetições de requisição podem ter cobrança não registrada; confira o saldo. Validação local pendente.

### Recuperação de JSON inválido do juiz

O avaliador valida cada resposta com Pydantic e tenta novamente até três vezes quando o JSON ou schema é inválido. Custos das respostas rejeitadas são registrados em `invalid_judgments.jsonl` e incluídos no orçamento na retomada. Avaliações válidas existentes são preservadas. Retome com `make evaluate RUN_ID=RUN-FULL01`. A falha anterior à correção não teve custo persistido; confira o saldo real. Validação local pendente.
