from enum import StrEnum

from pydantic import BaseModel, Field


class ProductOrders(BaseModel):
    tech: str = Field(description="Consigne pour le manager Tech")
    marketing: str = Field(description="Consigne pour le manager Marketing")


class TechOrders(BaseModel):
    backend: str = Field(description="Consigne pour le développeur backend")
    frontend: str = Field(description="Consigne pour le développeur frontend")


class MarketingOrders(BaseModel):
    email: str = Field(description="Consigne pour le chargé de communication")
    doc: str = Field(description="Consigne pour le rédacteur de l'aide en ligne")


class Status(StrEnum):
    READY = "ready"
    AT_RISK = "at_risk"
    BLOCKED = "blocked"


class Report(BaseModel):
    status: Status
    summary: str = Field(description="Ce qui est prêt ou ce qui bloque, en une ou deux phrases")
    risks: list[str]


class LaunchDecision(BaseModel):
    go: bool
    launch_date: str = Field(description="Date retenue, la date demandée ou une date reportée")
    reason: str
