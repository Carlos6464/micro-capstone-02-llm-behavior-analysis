# Análise experimental — RUN-FULL01

## Evidência e integridade

Arquivo fornecido: full_results.zip. SHA-256: `3502603f76eb23939fded0f6b6c3ba6308ce4780b6c1345f79882f5feca0cecf`.
450 respostas válidas, 450 avaliações individuais e 450 pares únicos. Os IDs correspondem exatamente ao manifesto e aos pares esperados. Há uma resposta de falha adicional. Isso comprova integridade estrutural, não rastreabilidade integral de configuração e julgamento.

## Resultados preliminares

| Prompt | SGD | Consistência (%) | TA (%) | P95 geração (s) | Delta SGD vs P01 | IC95% bootstrap |
|---|---:|---:|---:|---:|---:|---|
| P01 | 98,45 | 97,56 | 0,00 | 2,71 | 0 | referência |
| P02 | 98,95 | 98,67 | 3,33 | 9,01 | +0,50 | [-0,66; 1,69] |
| P03 | 97,48 | 97,44 | 3,33 | 2,77 | -0,98 | [-2,90; 0,62] |
| P04 | 97,67 | 98,33 | 3,33 | 8,62 | -0,79 | [-2,11; 0,37] |
| P05 | 98,39 | 99,33 | 1,11 | 2,83 | -0,07 | [-1,62; 1,22] |

SGD recalculado por caso a partir das avaliações auditadas e dos pares. Bootstrap pareado por 30 casos, 10.000 reamostragens, random.Random(42), percentis empíricos por posição. P95 por interpolação linear. Todos os intervalos incluem zero; não há evidência conclusiva de superioridade. As cinco estratégias estão dentro de dois pontos do maior SGD.

## Auditoria financeira

TC-024: mensal R$ 408,80; anual R$ 4.277,40. P01 e P05 acertaram 3/3 cada. P02, P03 e P04 erraram 3/3 cada, incluindo P03-3 que apresenta valor correto e incorreto. Total: 9/15 respostas com erro ou contradição. Par crítico sinalizado: TC-024-P03-1:TC-024-P03-3. Não equivale automaticamente a violação S4.

## Custos

Geração US$ 0,696658; individual US$ 1,2069631; pares US$ 0,8928576; JSON rejeitado US$ 0,0048702. Total registrado US$ 2,8013489. Não inclui falhas anteriores sem registro de custo nem pilotos.

## Pendências e decisão

81 avaliações individuais obrigatoriamente sinalizadas e 7 pares sinalizados; 22 registros individuais com alertas de auditoria. Ainda é necessário incluir amostra estratificada adicional e revisar evidências contra respostas e base de conhecimento. Nenhuma aprovação humana presumida. Todos os prompts permanecem INCONCLUSIVO até revisão e rastreabilidade integral. P01 e P05 são candidatos preliminares, não recomendações de produção. Dataset sintético e juiz da mesma família do gerador limitam generalização. Nenhuma chamada paga adicional nesta análise. Arquivo original não publicado neste commit.
