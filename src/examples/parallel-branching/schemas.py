from enum import StrEnum

from pydantic import BaseModel, Field


class Language(StrEnum):
    EN = "en"
    ES = "es"
    DE = "de"


class Message(BaseModel):
    key: str = Field(description="Clé i18n, recopiée telle quelle")
    text: str


class Translation(BaseModel):
    messages: list[Message]


class PlaceholderMismatch(BaseModel):
    language: Language
    key: str
    expected: set[str]
    found: set[str]
