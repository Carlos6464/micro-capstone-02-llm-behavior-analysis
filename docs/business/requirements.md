# Requisitos da solução

## Requisitos de negócio

| ID | Requisito | Prioridade |
|---|---|---|
| RN-001 | Avaliar a viabilidade de LLMs no atendimento corporativo | Alta |
| RN-002 | Utilizar cenários representativos de atendimento | Alta |
| RN-003 | Garantir aderência às políticas empresariais como objetivo de avaliação | Alta |
| RN-004 | Identificar riscos de informações incorretas ou inventadas | Alta |
| RN-005 | Avaliar consistência das respostas | Alta |
| RN-006 | Comparar estratégias de engenharia de prompts | Alta |
| RN-007 | Garantir rastreabilidade dos resultados | Alta |
| RN-008 | Produzir recomendação baseada em evidências | Alta |
| RN-009 | Investigar custos operacionais e latência | Média |
| RN-010 | Apoiar decisão sobre futura implantação | Alta |

## Requisitos funcionais

| ID | Requisito |
|---|---|
| RF-001 | Carregar dataset com pelo menos 15 perguntas de clientes |
| RF-002 | Disponibilizar base de conhecimento corporativa |
| RF-003 | Gerenciar cinco estratégias distintas de prompts |
| RF-004 | Executar todas as estratégias sobre o mesmo dataset |
| RF-005 | Permitir múltiplas execuções por combinação experimental |
| RF-006 | Registrar respostas originais do modelo |
| RF-007 | Avaliar respostas conforme critérios predefinidos |
| RF-008 | Consolidar resultados por estratégia |
| RF-009 | Gerar tabelas e gráficos comparativos |
| RF-010 | Disponibilizar evidências para os relatórios |

## Requisitos não funcionais

| ID | Categoria | Requisito |
|---|---|---|
| RNF-001 | Segurança | Não armazenar credenciais no repositório |
| RNF-002 | Privacidade | Utilizar dados simulados ou anonimizados |
| RNF-003 | Reprodutibilidade | Registrar modelo, versão disponível e parâmetros |
| RNF-004 | Rastreabilidade | Identificar individualmente cada execução |
| RNF-005 | Manutenibilidade | Adotar arquitetura modular |
| RNF-006 | Extensibilidade | Permitir novas estratégias de prompts |
| RNF-007 | Confiabilidade | Registrar falhas e erros de execução |
| RNF-008 | Portabilidade | Executar em ambientes compatíveis com Python |
| RNF-009 | Auditabilidade | Preservar evidências experimentais |
| RNF-010 | Documentação | Documentar decisões e procedimentos |

Os requisitos serão associados a componentes e testes nas etapas seguintes. Nenhum requisito é considerado validado nesta etapa.
