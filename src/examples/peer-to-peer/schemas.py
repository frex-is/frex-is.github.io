from enum import StrEnum

from pydantic import BaseModel, Field


class Peer(StrEnum):
    CLIENT = "client"
    FREELANCE = "freelance"
    SENIOR = "senior"


class ClientContact(StrEnum):
    FREELANCE = Peer.FREELANCE


class FreelanceContact(StrEnum):
    CLIENT = Peer.CLIENT
    SENIOR = Peer.SENIOR


class SeniorContact(StrEnum):
    FREELANCE = Peer.FREELANCE


class Status(StrEnum):
    NEGOTIATING = "negotiating"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class NegotiatorMessage(BaseModel):
    content: str = Field(description="Ton message, en 1 à 3 phrases")
    status: Status = Field(description="accepted ou rejected seulement si tu clos la négociation")


class ClientMessage(NegotiatorMessage):
    to: ClientContact


class FreelanceMessage(NegotiatorMessage):
    to: FreelanceContact


class SeniorMessage(BaseModel):
    to: SeniorContact
    content: str = Field(description="Ton avis, en 1 à 3 phrases")
