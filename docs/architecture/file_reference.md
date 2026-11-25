# Referência técnica arquivo por arquivo

**Autor:** Carlos Adriano · **Data:** 25/11/2026

Inventário da árvore versionada em 9a3e6e8, incluindo arquivos de código, testes, configuração, dados, documentação e marcadores. As descrições distinguem implementação atual de funcionalidades planejadas.

| Arquivo (link direto) | Responsabilidade e funcionamento |
|---|---|
| [`.env.example`](../../.env.example) | Modelo de variáveis de ambiente para geração, juiz, orçamento e log; não contém chaves reais. |
| [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) | Workflow de push/PR para main: checkout, uv, Python 3.12, sync, validate, pytest com cobertura e Ruff. Não exige 85% nem usa lockfile ainda. |
| [`.gitignore`](../../.gitignore) | Regras de exclusão de arquivos locais e temporários; revisar antes de gerar resultados ou versionar lockfile. |
| [`.python-version`](../../.python-version) | Seleciona Python 3.12. |
| [`README.md`](../../README.md) | Apresentação, escopo, arquitetura, indicadores, roadmap e links de documentação. |
| [`config/.gitkeep`](../../config/.gitkeep) | Marcador para manter diretório vazio no Git; não é consumido pelo pipeline. |
| [`config/evaluation_config.yaml`](../../config/evaluation_config.yaml) | Pesos, limiares, amostragem e estatística aprovados; código atual ainda replica parte dos valores em constantes. |
| [`config/experiment_config.yaml`](../../config/experiment_config.yaml) | Parâmetros de geração e planejamento consumidos por load_config. |
| [`config/pricing_config.yaml`](../../config/pricing_config.yaml) | Preços por milhão de tokens de geração e juiz; valores nulos bloqueiam execução real até preenchimento. |
| [`data/knowledge_base/.gitkeep`](../../data/knowledge_base/.gitkeep) | Marcador para manter diretório vazio no Git; não é consumido pelo pipeline. |
| [`data/knowledge_base/README.md`](../../data/knowledge_base/README.md) | Índice e ordem dos documentos corporativos. |
| [`data/knowledge_base/billing_policy.md`](../../data/knowledge_base/billing_policy.md) | Pagamentos, cobrança, reembolsos e limites. |
| [`data/knowledge_base/cancellation_policy.md`](../../data/knowledge_base/cancellation_policy.md) | Cancelamento e condições contratuais. |
| [`data/knowledge_base/customer_service_policy.md`](../../data/knowledge_base/customer_service_policy.md) | Regras de comunicação e atendimento. |
| [`data/knowledge_base/escalation_matrix.md`](../../data/knowledge_base/escalation_matrix.md) | Encaminhamento por área e prioridade. |
| [`data/knowledge_base/knowledge_governance.md`](../../data/knowledge_base/knowledge_governance.md) | Governança e versionamento da KB; excluído do contexto runtime. |
| [`data/knowledge_base/operational_procedures.md`](../../data/knowledge_base/operational_procedures.md) | Procedimentos operacionais POP. |
| [`data/knowledge_base/plans_and_pricing.md`](../../data/knowledge_base/plans_and_pricing.md) | Planos, preços, usuários e regras comerciais. |
| [`data/knowledge_base/product_catalog.md`](../../data/knowledge_base/product_catalog.md) | Módulos, recursos e limitações do produto. |
| [`data/knowledge_base/security_policy.md`](../../data/knowledge_base/security_policy.md) | Credenciais, autorização, privacidade e retenção. |
| [`data/knowledge_base/support_policy.md`](../../data/knowledge_base/support_policy.md) | Horários, prioridades e SLA de resposta. |
| [`data/processed/.gitkeep`](../../data/processed/.gitkeep) | Marcador para manter diretório vazio no Git; não é consumido pelo pipeline. |
| [`data/processed/README.md`](../../data/processed/README.md) | Instruções e contexto do benchmark. |
| [`data/processed/benchmark_dataset.csv`](../../data/processed/benchmark_dataset.csv) | Visão tabular combinada para inspeção humana. |
| [`data/processed/benchmark_expectations.jsonl`](../../data/processed/benchmark_expectations.jsonl) | Referências esperadas, categorias, riscos e políticas para o juiz; não são enviadas ao gerador. |
| [`data/processed/benchmark_inputs.jsonl`](../../data/processed/benchmark_inputs.jsonl) | 30 perguntas e canais, entradas do gerador. |
| [`data/processed/dataset_manifest.json`](../../data/processed/dataset_manifest.json) | Metadados, versão e aprovação do dataset sintético. |
| [`data/raw/.gitkeep`](../../data/raw/.gitkeep) | Marcador para manter diretório vazio no Git; não é consumido pelo pipeline. |
| [`docs/architecture/.gitkeep`](../../docs/architecture/.gitkeep) | Marcador para manter diretório vazio no Git; não é consumido pelo pipeline. |
| [`docs/architecture/application_flow.md`](../../docs/architecture/application_flow.md) | Guia de fluxo e comandos. |
| [`docs/assets/banner.svg`](../../docs/assets/banner.svg) | Banner visual do README. |
| [`docs/business/.gitkeep`](../../docs/business/.gitkeep) | Marcador para manter diretório vazio no Git; não é consumido pelo pipeline. |
| [`docs/business/business_case.md`](../../docs/business/business_case.md) | Justificativa da iniciativa. |
| [`docs/business/business_context.md`](../../docs/business/business_context.md) | Cenário e premissas operacionais. |
| [`docs/business/company_profile.md`](../../docs/business/company_profile.md) | Perfil da empresa fictícia. |
| [`docs/business/requirements.md`](../../docs/business/requirements.md) | Requisitos de negócio, funcionais e não funcionais. |
| [`docs/business/risk_assessment.md`](../../docs/business/risk_assessment.md) | Riscos da iniciativa. |
| [`docs/business/scope.md`](../../docs/business/scope.md) | Escopo e exclusões. |
| [`docs/business/stakeholders.md`](../../docs/business/stakeholders.md) | Partes interessadas simuladas. |
| [`docs/business/success_criteria.md`](../../docs/business/success_criteria.md) | Critérios de sucesso. |
| [`docs/decisions/.gitkeep`](../../docs/decisions/.gitkeep) | Marcador para manter diretório vazio no Git; não é consumido pelo pipeline. |
| [`docs/decisions/ADR-001-knowledge-base-strategy.md`](../../docs/decisions/ADR-001-knowledge-base-strategy.md) | Decisão de contexto direto sem RAG. |
| [`docs/decisions/ADR-002-dataset-design.md`](../../docs/decisions/ADR-002-dataset-design.md) | Decisão de desenho do dataset. |
| [`docs/decisions/ADR-003-prompt-strategy.md`](../../docs/decisions/ADR-003-prompt-strategy.md) | Decisão das cinco estratégias. |
| [`docs/decisions/ADR-004-evaluation-strategy.md`](../../docs/decisions/ADR-004-evaluation-strategy.md) | Decisão de avaliação híbrida. |
| [`docs/decisions/ADR-005-software-architecture.md`](../../docs/decisions/ADR-005-software-architecture.md) | Decisão de arquitetura modular. |
| [`docs/methodology/.gitkeep`](../../docs/methodology/.gitkeep) | Marcador para manter diretório vazio no Git; não é consumido pelo pipeline. |
| [`docs/methodology/dataset_card.md`](../../docs/methodology/dataset_card.md) | Ficha técnica do benchmark. |
| [`docs/methodology/decision_framework.md`](../../docs/methodology/decision_framework.md) | Regras GO, condicional e NO-GO. |
| [`docs/methodology/evaluation_framework.md`](../../docs/methodology/evaluation_framework.md) | Dimensões e estrutura da avaliação. |
| [`docs/methodology/evaluation_protocol.md`](../../docs/methodology/evaluation_protocol.md) | Procedimento de avaliação e revisão. |
| [`docs/methodology/evaluation_rubrics.md`](../../docs/methodology/evaluation_rubrics.md) | Rubricas de notas. |
| [`docs/methodology/hallucination_taxonomy.md`](../../docs/methodology/hallucination_taxonomy.md) | Classificação de alucinações. |
| [`docs/methodology/metrics_definition.md`](../../docs/methodology/metrics_definition.md) | Definições e fórmulas de métricas. |
| [`docs/methodology/prompt_engineering.md`](../../docs/methodology/prompt_engineering.md) | Metodologia das estratégias. |
| [`docs/methodology/security_violation_taxonomy.md`](../../docs/methodology/security_violation_taxonomy.md) | Tipos e severidades de violações. |
| [`docs/methodology/statistical_analysis.md`](../../docs/methodology/statistical_analysis.md) | Método estatístico e limitações. |
| [`docs/operations/setup_guide.md`](../../docs/operations/setup_guide.md) | Instalação e execução local. |
| [`prompts/.gitkeep`](../../prompts/.gitkeep) | Marcador para manter diretório vazio no Git; não é consumido pelo pipeline. |
| [`prompts/README.md`](../../prompts/README.md) | Catálogo e orientações de prompts. |
| [`prompts/consistency_judge.txt`](../../prompts/consistency_judge.txt) | Instruções de equivalência entre respostas. |
| [`prompts/evaluation_judge.txt`](../../prompts/evaluation_judge.txt) | Instruções de avaliação individual. |
| [`prompts/p01_baseline.txt`](../../prompts/p01_baseline.txt) | Instrução simples de referência. |
| [`prompts/p02_role.txt`](../../prompts/p02_role.txt) | Definição do papel de atendimento. |
| [`prompts/p03_structured.txt`](../../prompts/p03_structured.txt) | Estrutura explícita da resposta. |
| [`prompts/p04_few_shot.txt`](../../prompts/p04_few_shot.txt) | Exemplos de atendimento. |
| [`prompts/p05_policy_constrained.txt`](../../prompts/p05_policy_constrained.txt) | Restrições e políticas explícitas. |
| [`prompts/prompt_registry.yaml`](../../prompts/prompt_registry.yaml) | Registro de IDs, versões, status e templates. |
| [`pyproject.toml`](../../pyproject.toml) | Metadados, restrição Python, dependências runtime/dev, configuração pytest e Ruff. |
| [`results/evaluated/.gitkeep`](../../results/evaluated/.gitkeep) | Marcador para manter diretório vazio no Git; não é consumido pelo pipeline. |
| [`results/raw/.gitkeep`](../../results/raw/.gitkeep) | Marcador para manter diretório vazio no Git; não é consumido pelo pipeline. |
| [`results/reports/.gitkeep`](../../results/reports/.gitkeep) | Marcador para manter diretório vazio no Git; não é consumido pelo pipeline. |
| [`src/__init__.py`](../../src/__init__.py) | Inicializador do pacote Python; não contém lógica operacional relevante. |
| [`src/__main__.py`](../../src/__main__.py) | Importa main de src.cli e o chama quando o pacote é executado com python -m src. |
| [`src/analytics/.gitkeep`](../../src/analytics/.gitkeep) | Marcador para manter diretório vazio no Git; não é consumido pelo pipeline. |
| [`src/analytics/__init__.py`](../../src/analytics/__init__.py) | Inicializador do pacote Python; não contém lógica operacional relevante. |
| [`src/analytics/decision_engine.py`](../../src/analytics/decision_engine.py) | decide retorna NO-GO para crítico confirmado; INCONCLUSIVO quando faltam cobertura, rastreabilidade, revisão ou grupos completos; aplica limiares GO e GO CONDICIONAL. CLI ainda usa parâmetros conservadores padrão. |
| [`src/analytics/metrics.py`](../../src/analytics/metrics.py) | normalize_score transforma 1–5 em 0–100; pair_score pondera fatos 40%, decisão 30%, orientação 20%, segurança 10%; global_score aplica pesos SGD; aggregate agrupa respostas e pares completos por caso e estratégia, calcula cobertura, alucinação, S4 e SGD. |
| [`src/analytics/ranking.py`](../../src/analytics/ranking.py) | rank seleciona apenas GO, agrupa empates até 2 pontos do maior SGD e ordena por segurança, alucinação, consistência, custo e latência. Ainda não conectado à CLI. |
| [`src/analytics/statistics.py`](../../src/analytics/statistics.py) | paired_bootstrap exige mesmos IDs de caso, calcula diferenças, reamostra com NumPy e retorna média e percentis 2,5/97,5. Ainda não conectado à CLI. |
| [`src/cli.py`](../../src/cli.py) | main(): interpreta argumentos com argparse; carrega dados, valida IDs e templates, filtra casos, cria tarefas, seleciona comando e diretórios. Instancia provedor somente em run/evaluate com --execute. Entrada: argumentos e arquivos; saída: JSON no terminal ou artefatos por RUN_ID. |
| [`src/core/__init__.py`](../../src/core/__init__.py) | Inicializador do pacote Python; não contém lógica operacional relevante. |
| [`src/core/config.py`](../../src/core/config.py) | ExperimentConfig define repetições, semente, estratégias, temperatura, top_p e limite de saída; load_config lê YAML e valida com Pydantic. |
| [`src/core/schemas.py`](../../src/core/schemas.py) | BenchmarkInput valida ID, canal e pergunta; BenchmarkExpectation contém fatos e políticas esperados; LLMMessage define papel e conteúdo; ExperimentTask identifica caso, prompt e repetição via execution_id. |
| [`src/data/__init__.py`](../../src/data/__init__.py) | Inicializador do pacote Python; não contém lógica operacional relevante. |
| [`src/data/dataset_loader.py`](../../src/data/dataset_loader.py) | load_inputs lê JSONL e verifica mínimo de 15 e IDs únicos; load_expectations lê referências separadas. A CLI compara os IDs dos dois conjuntos. |
| [`src/data/knowledge_loader.py`](../../src/data/knowledge_loader.py) | load_knowledge concatena os nove documentos runtime em ordem fixa, com separadores de arquivo. Não realiza busca vetorial. |
| [`src/evaluation/.gitkeep`](../../src/evaluation/.gitkeep) | Marcador para manter diretório vazio no Git; não é consumido pelo pipeline. |
| [`src/evaluation/__init__.py`](../../src/evaluation/__init__.py) | Inicializador do pacote Python; não contém lógica operacional relevante. |
| [`src/evaluation/evaluation_runner.py`](../../src/evaluation/evaluation_runner.py) | Scores, Judgment e PairJudgment validam notas e equivalências. evaluate lê respostas bem-sucedidas, agrupa por caso/estratégia e gera pares; judge monta mensagens separadas, verifica orçamento, chama provedor e valida JSON. Registra avaliações e sinaliza revisão. Não implementa avaliação determinística completa. |
| [`src/evaluation/human_review.py`](../../src/evaluation/human_review.py) | review_queue seleciona registros obrigatórios e arredonda para cima 20% dos demais por estrato estratégia/categoria, usando semente 42. Retorna lista para exportação; não importa decisões humanas. |
| [`src/experiments/.gitkeep`](../../src/experiments/.gitkeep) | Marcador para manter diretório vazio no Git; não é consumido pelo pipeline. |
| [`src/experiments/__init__.py`](../../src/experiments/__init__.py) | Inicializador do pacote Python; não contém lógica operacional relevante. |
| [`src/experiments/experiment_plan.py`](../../src/experiments/experiment_plan.py) | plan gera produto cartesiano de casos, estratégias e repetições, valida IDs únicos e embaralha com random.Random(seed). Retorna lista de ExperimentTask. |
| [`src/experiments/experiment_runner.py`](../../src/experiments/experiment_runner.py) | ExperimentRunner recebe provedor, diretório, orçamento e limite de saída. run lê registros existentes, bloqueia tentativas incertas, pula sucessos, monta mensagens, verifica orçamento, registra tentativa, chama provedor e persiste resposta, tokens, latência e hashes. Falhas interrompem execução; não há retries automáticos. |
| [`src/infrastructure/__init__.py`](../../src/infrastructure/__init__.py) | Inicializador do pacote Python; não contém lógica operacional relevante. |
| [`src/infrastructure/cost_tracker.py`](../../src/infrastructure/cost_tracker.py) | CostTracker valida preços e limite; cost calcula (tokens entrada × preço entrada + tokens saída × preço saída)/1 milhão; check bloqueia estimativa acima do limite; record acumula custo ou interrompe se tokens desconhecidos. Não garante teto absoluto de cobrança. |
| [`src/infrastructure/hashing.py`](../../src/infrastructure/hashing.py) | sha256 recebe texto UTF-8 e retorna digest hexadecimal para identificação de conteúdo. |
| [`src/infrastructure/storage.py`](../../src/infrastructure/storage.py) | read_records retorna lista de objetos JSONL ou lista vazia; append_record acrescenta linha JSON, flush e fsync. Não oferece transação entre arquivos nem bloqueio concorrente. |
| [`src/prompting/__init__.py`](../../src/prompting/__init__.py) | Inicializador do pacote Python; não contém lógica operacional relevante. |
| [`src/prompting/prompt_builder.py`](../../src/prompting/prompt_builder.py) | build_messages valida ocorrência única dos três placeholders e marcador final; injeta KB e canal na mensagem system e mantém pergunta na mensagem user. |
| [`src/prompting/prompt_registry.py`](../../src/prompting/prompt_registry.py) | load_prompts lê prompt_registry.yaml, seleciona templates aprovados e exige P01–P05. |
| [`src/providers/.gitkeep`](../../src/providers/.gitkeep) | Marcador para manter diretório vazio no Git; não é consumido pelo pipeline. |
| [`src/providers/__init__.py`](../../src/providers/__init__.py) | Inicializador do pacote Python; não contém lógica operacional relevante. |
| [`src/providers/base.py`](../../src/providers/base.py) | ProviderResponse é dataclass imutável com texto, modelo, tokens e ID; LLMProvider é Protocol que exige generate(messages). Permite injetar outros provedores sem alterar runner. |
| [`src/providers/factory.py`](../../src/providers/factory.py) | create_provider lê LLM_API_KEY/LLM_MODEL ou JUDGE_API_KEY/JUDGE_MODEL, instancia OpenAI com timeout 60 e retries SDK desativados, devolve OpenAIProvider. |
| [`src/providers/openai_provider.py`](../../src/providers/openai_provider.py) | OpenAIProvider guarda cliente e parâmetros; generate chama chat.completions.create, rejeita saída vazia ou incompleta e converte retorno em ProviderResponse. Compatibilidade dos parâmetros depende do modelo escolhido. |
| [`src/reporting/__init__.py`](../../src/reporting/__init__.py) | Inicializador do pacote Python; não contém lógica operacional relevante. |
| [`src/reporting/report_generator.py`](../../src/reporting/report_generator.py) | report normaliza registros com Pandas, grava strategy_metrics.csv e decision_summary.json, e usa Matplotlib Agg para sgd.png se houver SGD válido. |
| [`tests/.gitkeep`](../../tests/.gitkeep) | Marcador para manter diretório vazio no Git; não é consumido pelo pipeline. |
| [`tests/unit/test_analytics.py`](../../tests/unit/test_analytics.py) | Testa normalização parametrizada, SGD máximo, equivalência total e bootstrap de diferença constante. |
| [`tests/unit/test_execution.py`](../../tests/unit/test_execution.py) | test_cost verifica cálculo e bloqueio de orçamento; test_storage verifica gravação e leitura JSONL em diretório temporário. |
| [`tests/unit/test_foundation.py`](../../tests/unit/test_foundation.py) | test_plan verifica 450 IDs únicos; test_messages verifica papéis system/user e preservação da pergunta. |
| [`docs/architecture/file_reference.md`](file_reference.md) | Inventário e referência técnica dos arquivos. |
| [`docs/architecture/software_architecture.md`](software_architecture.md) | Arquitetura, dependências, contratos e sequência de execução. |

[Arquitetura detalhada](software_architecture.md) · [Fluxo e comandos](application_flow.md) · [README](../../README.md)

## Novos testes e automação

| Arquivo | Responsabilidade |
|---|---|
| [Makefile](../../Makefile) | Validação local e log, com limite de cobertura. |
| [uv.lock](../../uv.lock) | Dependências resolvidas e versionadas. |
| [test_decisions.py](../../tests/unit/test_decisions.py) | Decisão e ranking. |
| [test_providers.py](../../tests/unit/test_providers.py) | Adaptador e fábrica com mocks. |
| [test_pipeline.py](../../tests/integration/test_pipeline.py) | Pipeline simulado, retomada, avaliação e relatório. |
| [test_cli.py](../../tests/integration/test_cli.py) | Comandos locais e bloqueio de chamadas reais. |
