# Relatório executivo — Nexus Cloud

**Data:** 25/11/2026 | **Experimento:** RUN-FULL01 | **Responsável:** Carlos Adriano

## Objetivo e escopo

Avaliar cinco formas de instrução para atendimento SaaS por chat e e-mail, utilizando Gemini 2.5 Flash, contexto corporativo comum e 30 cenários sintéticos, com três repetições independentes por estratégia. A empresa e os dados são simulados. Não houve implantação em produção.

## Resultados

| Estratégia | SGD | Consistência | Alucinação | P95 geração |
|---|---:|---:|---:|---:|
| P01 Baseline | 98,45 | 97,56% | 0,00% | 2,71 s |
| P02 Role | 98,95 | 98,67% | 3,33% | 9,01 s |
| P03 Estruturado | 97,48 | 97,44% | 3,33% | 2,77 s |
| P04 Few-shot | 97,67 | 98,33% | 3,33% | 8,62 s |
| P05 Restrições | 98,39 | 99,33% | 1,11% | 2,83 s |

Fonte: [análise experimental registrada](full_experiment_analysis.md). Indicadores auditados preliminares, não corrigidos por revisão humana individual. 450 respostas, 450 avaliações individuais e 450 pares. Custo registrado US$ 2,8013489, excluindo pilotos e falhas sem custo persistido.

## Interpretação e recomendação

P02 lidera o SGD bruto, mas todas as estratégias estão dentro da margem prática de dois pontos. Os intervalos bootstrap pareados incluem zero. Não há evidência suficiente de superioridade. P01 é candidato de referência por menor taxa de alucinação observada e menor P95; P05 é alternativa pela consistência. P02, P03 e P04 erraram as três repetições financeiras do TC-024. Recomenda-se cálculo determinístico externo ao LLM, encaminhamento humano para decisões sensíveis e monitoramento de evidências. Não alterar retrospectivamente os prompts ou dados coletados.

## Decisão de governança

**INCONCLUSIVO para homologação formal de todas as estratégias.** Recomendação exploratória: manter P01 e P05 para eventual piloto controlado após aprovação dos controles. Não autorizar produção. O responsável informou ter revisado os resultados e solicitou prosseguir sem planilha; não foram fornecidas decisões individuais, correções ou evidência verificável de homologação. Não se presume confirmação de nenhum registro. A contradição crítica sinalizada no TC-024/P03 permanece sem decisão documentada. A rastreabilidade integral e os testes da última versão permanecem pendentes. Não houve novas chamadas pagas.

## Limitações

Cenários sintéticos, juiz da mesma família do gerador, evidências não literais, amostra limitada, ausência de validação humana item a item documentada e custos estimados. Os resultados não representam garantia de desempenho real. A publicação do relatório não equivale à homologação do software ou do atendimento.
