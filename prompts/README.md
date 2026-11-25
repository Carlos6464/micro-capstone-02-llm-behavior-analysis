# Catálogo de prompts

Cinco estratégias aprovadas, versão 1.0.0.

- [P01 — baseline](p01_baseline.txt)
- [P02 — role](p02_role.txt)
- [P03 — structured](p03_structured.txt)
- [P04 — few_shot](p04_few_shot.txt)
- [P05 — policy_constrained](p05_policy_constrained.txt)

[Registro de versões](prompt_registry.yaml). Preencher knowledge_base e channel na mensagem de sistema; enviar customer_query separadamente como mensagem de usuário, usando o marcador PERGUNTA DO CLIENTE como fronteira do template. Não enviar expectativas de avaliação. Não executar ferramentas externas.

## Instrumentos de avaliação (não são estratégias experimentais)

[Juiz individual](evaluation_judge.txt) · [Juiz de consistência](consistency_judge.txt). [Configuração](../config/evaluation_config.yaml) · [Framework](../docs/methodology/evaluation_framework.md).
