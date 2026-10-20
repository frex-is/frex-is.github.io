from dataclasses import dataclass
from enum import StrEnum

from pydantic import BaseModel, Field


class CustomerTier(StrEnum):
    STANDARD = "standard"
    LOYAL = "loyal"


@dataclass(frozen=True)
class CartTestCase:
    description: str
    prices: list[float]
    customer_tier: CustomerTier
    expected_total: float


class GeneratedCode(BaseModel):
    code: str = Field(
        description="Le module Python complet : constantes éventuelles + la fonction cart_total. Sans import de CustomerTier."
    )


class NamingIssue(BaseModel):
    subject: str = Field(description="Le nom ou la valeur en cause, tel qu'il apparaît dans le code (ex. `t`, `0.9`)")
    problem: str = Field(description="Ce qui manque côté intention métier, en une phrase")
    suggestion: str = Field(description="Le nom ou la constante proposée")


class IntentReview(BaseModel):
    issues: list[NamingIssue] = Field(description="Vide si chaque nom et chaque valeur dit son intention métier")
