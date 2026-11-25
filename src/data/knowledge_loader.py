from pathlib import Path

DOCUMENTS = (
    "product_catalog.md", "plans_and_pricing.md", "billing_policy.md",
    "cancellation_policy.md", "support_policy.md", "security_policy.md",
    "operational_procedures.md", "customer_service_policy.md", "escalation_matrix.md",
)


def load_knowledge(root: Path) -> str:
    directory = root / "data/knowledge_base"
    return "\n\n".join(
        f"--- {name} ---\n{(directory / name).read_text(encoding='utf-8')}"
        for name in DOCUMENTS
    )
