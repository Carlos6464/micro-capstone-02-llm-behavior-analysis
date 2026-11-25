# Engenharia de prompts

## Desenho experimental

P01: referência mínima; P02: papel e tom; P03: estrutura de saída; P04: cinco demonstrações fixas; P05: reforço de políticas. Hipóteses: respectivamente referência, adequação corporativa, clareza/completude, aprendizagem em contexto e redução de violações. Não são resultados observados.

Mesmo modelo, base KB-NEXUS-001 v1.0.0, dataset DS-NEXUS-001 aprovado, canal e hierarquia de mensagens. Mensagem de sistema: instruções, contexto e canal; mensagem de usuário: pergunta. Sem histórico ou ferramentas externas. Três repetições independentes: 30 × 5 × 3 = 450 respostas previstas. Temperatura 0,2, top-p 1,0 e limite de saída 1024 tokens propostos, sujeitos ao suporte do modelo. Provedor inicial OpenAI, modelo a definir. Registrar parâmetros efetivos, versão e hash dos templates na execução.

## Few-shot

FS-001 catálogo de produtos; FS-002 COM-006; FS-003 FIN-005 e FIN-011; FS-004 planos e COM-009; FS-005 SEG-003 e SEG-006. Exemplos fixos, distintos textualmente dos 30 casos, com possíveis semelhanças temáticas. Não utilizar respostas de referência do benchmark na composição. Não há treinamento de pesos.

## Validação desta etapa

Cinco templates, três variáveis únicas em cada, sufixo comum, cinco exemplos sem coincidência textual exata com as entradas, 150 composições verificadas sem chamadas de API. Base recuperada dos nove documentos corporativos. Testes permanentes, hashes, validação do provedor e execução real ficam para implementação. Diferenças de comprimento e instruções impedem atribuir efeitos a tokens isolados; comparar estratégias completas. Dataset sintético aprovado, sem origem real individual comprovada.
