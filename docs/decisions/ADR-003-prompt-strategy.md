# ADR-003 — Estratégias de engenharia de prompts

**Status:** aprovado.

## Contexto
Comparar cinco estratégias de atendimento sob condições comuns.

## Decisão
Templates externos versionados em texto, registro YAML, contexto direto comum, pergunta em mensagem de usuário separada, cinco exemplos fixos independentes das perguntas do benchmark, saída em texto natural. Composição direta em Python, sem LangChain. Não otimizar antes da avaliação inicial.

## Consequências
Rastreabilidade e manutenção simplificadas; custo de contexto e extensão variam entre estratégias. Restrições não garantem segurança. Hashes e testes de integração serão implementados no pipeline.
