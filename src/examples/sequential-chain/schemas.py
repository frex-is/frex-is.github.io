from enum import StrEnum

from pydantic import BaseModel, Field


class Commit(BaseModel):
    sha: str
    message: str


class ChangeCategory(StrEnum):
    FEATURE = "feature"
    FIX = "fix"
    INTERNAL = "internal"


class Change(BaseModel):
    sha: str
    category: ChangeCategory
    summary: str = Field(description="Ce qui change pour l'utilisateur, en une phrase")


class Triage(BaseModel):
    changes: list[Change]


class ReleaseNotes(BaseModel):
    features: list[str]
    fixes: list[str]


class Announcement(BaseModel):
    text: str
