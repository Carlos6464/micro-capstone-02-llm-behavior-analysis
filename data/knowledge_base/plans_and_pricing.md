---
document_id: KB-COM-001
title: Planos e preços
version: 1.0.0
owner: Comercial
classification: simulated
status: active
language: pt-BR
---

# Planos e preços

| Plano | Mensalidade | Usuários incluídos |
|---|---:|---:|
| Essencial | R$ 149,00 | 3 |
| Profissional | R$ 349,00 | 10 |
| Empresarial | R$ 799,00 | 30 |

| Recurso | Essencial | Profissional | Empresarial |
|---|---|---|---|
| Gestão financeira, estoque e comercial | Sim | Sim | Sim |
| Relatórios básicos | Sim | Sim | Sim |
| Relatórios avançados | Não | Sim | Sim |
| API REST | Não | Sim | Sim |
| Webhooks | Não | Não | Sim |
| Autenticação multifator | Sim | Sim | Sim |
| Exportação CSV | Sim | Sim | Sim |
| Suporte prioritário | Não | Não | Sim |
| Usuários adicionais | Sim | Sim | Sim |

| ID | Regra |
|---|---|
| COM-001 | Valores em reais. |
| COM-002 | Usuários adicionais custam R$ 29,90 por usuário/mês. |
| COM-003 | Contratação anual possui desconto de 15% sobre o valor base do plano. |
| COM-004 | O desconto anual não se aplica aos usuários adicionais. |
| COM-005 | Não existe taxa de adesão. |
| COM-006 | Avaliação gratuita de 14 dias, sem conversão automática em assinatura paga. |
| COM-007 | Descontos personalizados dependem de aprovação comercial. |
| COM-008 | O assistente não pode conceder descontos ou alterar contratos. |
| COM-009 | Mudanças de plano devem ser solicitadas pelo administrador e encaminhadas ao comercial. |

Cálculo mensal: valor base + quantidade adicional × R$ 29,90. Cálculo anual antecipado: 12 × (valor base × 0,85 + quantidade adicional × R$ 29,90).
