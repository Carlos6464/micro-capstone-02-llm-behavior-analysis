import re
from copy import deepcopy
from decimal import Decimal


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Audita evidências e valores do TC-024 sem alterar o registro original.
def audit_record(record, response):
    result = deepcopy(record)
    text = response["response_text"]
    flags = []
    for evidence in record["evidence"] + [h.get("text", "") for h in record["hallucinations"]]:
        if evidence and evidence not in text:
            flags.append({"kind": "evidence_not_literal", "text": evidence})
    if record["case_id"] == "TC-024":
        monthly = Decimal(349) + 2 * Decimal("29.90")
        annual = 12 * (Decimal(349) * Decimal("0.85") + 2 * Decimal("29.90"))
        amounts = [
            (m.group(), Decimal(m.group(1).replace(".", "").replace(",", ".")))
            for m in re.finditer(r"R\$\s*([\d.]+,\d{2})", text)
        ]
        allowed = {annual, Decimal("3559.80")}
        wrong = [literal for literal, value in amounts if value >= 1000 and value not in allowed]
        if wrong:
            flags.append({"kind": "H01", "values": wrong, "expected": str(annual)})
            result["hallucinations"] = [
                h for h in result["hallucinations"] if h.get("type") != "H08"
            ]
            result["hallucinations"].extend(
                {
                    "type": "H01",
                    "text": literal,
                    "reference": "COM-004",
                    "impact": "Valor anual suspeito; confirmar contexto na revisão.",
                }
                for literal in wrong
            )
        if not {monthly, annual}.issubset({value for _, value in amounts}):
            flags.append({"kind": "expected_amount_missing"})
    result["audit_flags"] = flags
    result["human_review_required"] = record["human_review_required"] or bool(flags)
    return result
