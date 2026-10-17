from enum import StrEnum

from pydantic import BaseModel, Field


class Issue(BaseModel):
    identifier: int
    title: str


class AgentName(StrEnum):
    JUNIOR = "junior"
    SENIOR = "senior"
    EXPERT = "expert"


class Bid(BaseModel):
    issue_identifier: int
    price: float = Field(description="Ton taux horaire × les heures qu'il te faudrait, à ton niveau")
    justification: str = Field(description="Une phrase")


class BidSheet(BaseModel):
    bids: list[Bid] = Field(description="Une offre pour chaque issue du pool")


class Resolution(BaseModel):
    summary: str
    steps: list[str]
