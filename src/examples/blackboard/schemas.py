from enum import StrEnum

from pydantic import BaseModel, Field


class AgentName(StrEnum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    VERIFIER = "verifier"
    REPORTER = "reporter"


class Status(StrEnum):
    OPEN = "open"
    CONFIRMED = "confirmed"
    REFUTED = "refuted"


class Entry(BaseModel):
    identifier: int
    author: AgentName
    statement: str
    status: Status = Status.OPEN
    evidence: str | None = None


class Board(BaseModel):
    version: int = 0
    symptom: str
    hypotheses: list[Entry] = []
    conclusion: str | None = None


class Hypothesis(BaseModel):
    statement: str = Field(description="Une cause possible du symptôme, en une phrase")


class Verdict(BaseModel):
    status: Status = Field(description="confirmed ou refuted")
    evidence: str = Field(description="L'extrait de preuve qui justifie le verdict, en une phrase")


class Conclusion(BaseModel):
    root_cause: str
    fix: str = Field(description="La correction à apporter, en une phrase")
