from dataclasses import dataclass
from math import isfinite


@dataclass
class CostTracker:
    limit: float
    input_price: float
    output_price: float
    spent: float = 0.0

    def __post_init__(self):
        if not all(isfinite(v) and v >= 0 for v in
                   (self.limit, self.input_price, self.output_price, self.spent)):
            raise ValueError("Orçamento ou preços inválidos.")

    def cost(self, input_tokens: int, output_tokens: int) -> float:
        return (input_tokens * self.input_price + output_tokens * self.output_price) / 1e6

    def check(self, estimated_input: int, maximum_output: int) -> None:
        if self.spent + self.cost(estimated_input, maximum_output) > self.limit:
            raise RuntimeError("Limite preventivo de orçamento atingido.")

    def record(self, input_tokens: int | None, output_tokens: int | None) -> float:
        if input_tokens is None or output_tokens is None:
            raise RuntimeError("Consumo desconhecido; interromper novas chamadas.")
        value = self.cost(input_tokens, output_tokens)
        self.spent += value
        return value
