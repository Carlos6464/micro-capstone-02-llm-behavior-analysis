from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class BenchmarkInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    case_id: str = Field(pattern=r"^TC-\d{3}$")
    channel: Literal["chat", "email"]
    customer_query: str = Field(min_length=1)


class BenchmarkExpectation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    case_id: str
    category: str
    risk_level: Literal["low", "medium", "high", "critical"]
    origin_type: Literal["synthetic"]
    source_id: str | None
    expected_behavior: str
    expected_facts: list[str]
    forbidden_behavior: list[str]
    knowledge_references: list[str]


class LLMMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ExperimentTask(BaseModel):
    case_id: str
    prompt_id: str
    repetition: int = Field(ge=1)

    @property
    def execution_id(self) -> str:
        return f"{self.case_id}-{self.prompt_id}-{self.repetition}"
