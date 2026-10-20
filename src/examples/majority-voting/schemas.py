from dataclasses import dataclass
from enum import StrEnum

from pydantic import BaseModel, Field


class Priority(StrEnum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class Voter(StrEnum):
    SUPPORT = "support"
    SRE = "sre"
    PRODUCT = "product"
    NEUTRAL = "neutral"


@dataclass(frozen=True)
class Ticket:
    number: int
    title: str
    description: str


class Vote(BaseModel):
    priority: Priority
    reason: str = Field(description="Pourquoi cette priorité, en une phrase, depuis ton angle")


class Outcome(StrEnum):
    RETAINED = "retained"
    ESCALATED = "escalated"


@dataclass(frozen=True)
class Verdict:
    leading_priority: Priority
    agreeing_votes: int
    outcome: Outcome
