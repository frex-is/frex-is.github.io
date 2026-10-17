from enum import StrEnum

from pydantic import BaseModel, Field


class AgentName(StrEnum):
    DIAGNOSTIC_ADVISOR = "diagnostic_advisor"
    INCIDENT_DETECTOR = "incident_detector"
    PUBLIC_COMMUNICATOR = "public_communicator"


class Topic(StrEnum):
    ALERT_FIRED = "alert.fired"
    RUNBOOK_SUGGESTED = "runbook.suggested"
    INCIDENT_OPENED = "incident.opened"
    STATUS_PUBLISHED = "status.published"


class Severity(StrEnum):
    WARNING = "warning"
    CRITICAL = "critical"


class AlertFired(BaseModel):
    alert_identifier: int
    source: str
    message: str
    severity: Severity


class RunbookSuggested(BaseModel):
    alert_identifier: int
    check: str


class IncidentOpened(BaseModel):
    title: str
    alert_identifiers: list[int]


class StatusPublished(BaseModel):
    message: str


class Runbook(BaseModel):
    check: str = Field(description="La première vérification à faire, en une phrase")


class Incident(BaseModel):
    title: str = Field(description="Le titre de l'incident, en une phrase")
    alert_identifiers: list[int] = Field(description="Les alertes liées à l'incident")


class Correlation(BaseModel):
    incident: Incident | None = Field(description="L'incident confirmé par les alertes reçues, null sinon")


class StatusMessage(BaseModel):
    message: str = Field(description="Le message public, en 1 à 2 phrases, sans jargon technique")


CONTRACTS = {
    Topic.ALERT_FIRED: AlertFired,
    Topic.RUNBOOK_SUGGESTED: RunbookSuggested,
    Topic.INCIDENT_OPENED: IncidentOpened,
    Topic.STATUS_PUBLISHED: StatusPublished,
}
