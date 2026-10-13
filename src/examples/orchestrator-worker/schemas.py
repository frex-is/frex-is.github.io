from enum import StrEnum

from pydantic import BaseModel, Field


class Issue(BaseModel):
    identifier: int
    title: str


class WorkerType(StrEnum):
    BUG = "bug"
    FEATURE = "feature"
    REFACTO = "refacto"


class Task(BaseModel):
    worker: WorkerType
    issue_identifiers: list[int] = Field(description="Issues traitées ensemble (doublons regroupés)")
    instructions: str = Field(description="Consigne précise pour le worker")


class Plan(BaseModel):
    tasks: list[Task]


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class BugReport(BaseModel):
    probable_cause: str
    fix_steps: list[str]
    severity: Severity


class FeatureSpec(BaseModel):
    user_story: str
    acceptance_criteria: list[str]


class RefactoPlan(BaseModel):
    problem: str
    steps: list[str]
    risks: list[str]
