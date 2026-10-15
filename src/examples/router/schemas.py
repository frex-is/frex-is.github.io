from enum import StrEnum

from pydantic import BaseModel, Field


class Difficulty(StrEnum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"
    UNCLEAR = "unclear"


class RoutingDecision(BaseModel):
    difficulty: Difficulty
    reason: str = Field(description="Pourquoi cette difficulté, en une phrase")


class QuickAnswer(BaseModel):
    answer: str = Field(description="Réponse en une ou deux phrases")
    snippet: str


class Diagnosis(BaseModel):
    cause: str
    fix: str
    snippet: str


class DesignOption(BaseModel):
    name: str
    tradeoffs: str


class DesignProposal(BaseModel):
    options: list[DesignOption]
    recommendation: str
