---
document_id: KB-ESC-001
title: Matriz de encaminhamento
version: 1.0.0
owner: Operações
classification: simulated
status: active
language: pt-BR
---

# Matriz de encaminhamento

| Situação | Área | Prioridade |
|---|---|---|
| Negociação de descontos | Comercial | Normal |
| Alteração contratual | Comercial | Normal |
| Cancelamento | Gestão de assinaturas | Normal |
| Cobrança duplicada | Financeiro | Normal |
| Reembolso | Financeiro | Normal |
| Falha técnica persistente | Suporte técnico | Conforme impacto |
| Indisponibilidade generalizada | Operações técnicas | Crítica |
| Suspeita de invasão | Segurança da Informação | Crítica |
| Exposição de dados | Segurança da Informação | Crítica |
| Solicitação LGPD | Proteção de dados | Prioritária |
| Reclamação grave | Experiência do Cliente | Prioritária |
| Informação não documentada | Área responsável | Conforme impacto |

```mermaid
flowchart TD
 A[Solicitação] --> B{Risco crítico?}
 B -->|Sim| C[Orientar encaminhamento imediato]
 B -->|Não| D{Informação disponível?}
 D -->|Não| E[Esclarecer ou encaminhar]
 D -->|Sim| F{Ação autorizada?}
 F -->|Não| G[Orientar atendimento humano]
 F -->|Sim| H[Responder ao cliente]
```

Encaminhamento é orientação textual, não transferência efetiva. Não inventar contatos, protocolos ou ações realizadas.
