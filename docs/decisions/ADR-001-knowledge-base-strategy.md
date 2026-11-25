# ADR-001 — Estratégia da base de conhecimento

**Status:** Aceita para a prova de conceito  
**Decisão:** Injeção direta de contexto consolidado, sem RAG.

## Contexto

Comparar cinco estratégias de engenharia de prompts sobre as mesmas perguntas e informações corporativas. A base é pequena e versionada.

## Alternativas

- Contexto direto: menor complexidade, conteúdo idêntico e rastreável.
- RAG com embeddings e banco vetorial: recuperação seletiva, porém introduz variabilidade adicional e infraestrutura.

## Decisão e consequências

Consolidar os nove documentos de conteúdo na ordem do índice, respeitando o limite de contexto do modelo. Registrar versão e hash do contexto efetivamente enviado. Manter modelo, versão disponível, parâmetros (incluindo temperatura quando configurável), perguntas e critérios iguais; histórico independente por execução. Variar a estrutura do prompt. P05 reforça as políticas já presentes no contexto comum.

O contexto direto aumenta o consumo de tokens conforme a base cresce. Verificar orçamento de contexto antes dos testes; não truncar silenciosamente. RAG poderá ser avaliado em evolução futura. A consolidação e o registro de integridade serão implementados posteriormente.

## Limitações

Não há garantia de aderência às políticas nem de segurança em produção. A base não contém dados reais e não é uma integração operacional.
