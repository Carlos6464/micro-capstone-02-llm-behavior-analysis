from src.core.schemas import BenchmarkInput, LLMMessage

MARKER = "\n\nPERGUNTA DO CLIENTE:\n{customer_query}"


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Compõe mensagens de sistema e usuário.
def build_messages(template: str, knowledge: str, case: BenchmarkInput) -> list[LLMMessage]:
    template = template.rstrip()
    if not template.endswith(MARKER):
        raise ValueError("Fronteira do template inválida.")
    for variable in ("knowledge_base", "channel", "customer_query"):
        if template.count("{" + variable + "}") != 1:
            raise ValueError(f"Variável inválida: {variable}")
    return [
        LLMMessage(
            role="system",
            content=template[: -len(MARKER)].format(knowledge_base=knowledge, channel=case.channel),
        ),
        LLMMessage(role="user", content=case.customer_query),
    ]
