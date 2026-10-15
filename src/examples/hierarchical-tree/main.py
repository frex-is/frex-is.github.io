import asyncio
from dataclasses import dataclass
from enum import StrEnum

from pydantic import BaseModel

from llm import AgentConfig, Effort, Model, call
from prompts import (
    BACKEND_PROMPT,
    DOC_PROMPT,
    EMAIL_PROMPT,
    FRONTEND_PROMPT,
    HEAD_DECISION_PROMPT,
    HEAD_PLAN_PROMPT,
    MARKETING_PLAN_PROMPT,
    MARKETING_SYNTHESIS_PROMPT,
    TECH_PLAN_PROMPT,
    TECH_SYNTHESIS_PROMPT,
)
from schemas import LaunchDecision, MarketingOrders, ProductOrders, Report, TechOrders


class Role(StrEnum):
    HEAD_OF_PRODUCT = "head_of_product"
    TECH = "tech"
    MARKETING = "marketing"
    BACKEND = "backend"
    FRONTEND = "frontend"
    EMAIL = "email"
    DOC = "doc"


@dataclass(frozen=True)
class Worker:
    role: Role
    agent: AgentConfig


@dataclass(frozen=True)
class Manager:
    role: Role
    planner: AgentConfig
    synthesizer: AgentConfig
    team: tuple["Manager | Worker", ...]


TREE = Manager(
    Role.HEAD_OF_PRODUCT,
    planner=AgentConfig(Model.OPUS, Effort.HIGH, HEAD_PLAN_PROMPT, ProductOrders),
    synthesizer=AgentConfig(Model.OPUS, Effort.HIGH, HEAD_DECISION_PROMPT, LaunchDecision),
    team=(
        Manager(
            Role.TECH,
            planner=AgentConfig(Model.SONNET, Effort.MEDIUM, TECH_PLAN_PROMPT, TechOrders),
            synthesizer=AgentConfig(Model.SONNET, Effort.MEDIUM, TECH_SYNTHESIS_PROMPT, Report),
            team=(
                Worker(Role.BACKEND, AgentConfig(Model.HAIKU, Effort.LOW, BACKEND_PROMPT, Report)),
                Worker(Role.FRONTEND, AgentConfig(Model.HAIKU, Effort.LOW, FRONTEND_PROMPT, Report)),
            ),
        ),
        Manager(
            Role.MARKETING,
            planner=AgentConfig(Model.SONNET, Effort.MEDIUM, MARKETING_PLAN_PROMPT, MarketingOrders),
            synthesizer=AgentConfig(Model.SONNET, Effort.MEDIUM, MARKETING_SYNTHESIS_PROMPT, Report),
            team=(
                Worker(Role.EMAIL, AgentConfig(Model.HAIKU, Effort.LOW, EMAIL_PROMPT, Report)),
                Worker(Role.DOC, AgentConfig(Model.HAIKU, Effort.LOW, DOC_PROMPT, Report)),
            ),
        ),
    ),
)

MISSION = "Lancer l'export CSV des factures le 1er novembre."

KNOWLEDGE = {
    Role.BACKEND: "Jusqu'à 80 000 factures par client. L'API ne pagine pas et coupe au-delà de 30 s.",
    Role.FRONTEND: "La page Factures a une barre d'actions. Le bouton du design system gère le chargement.",
    Role.EMAIL: "L'outil d'emailing est configuré. Les clients Pro représentent 1 200 comptes.",
    Role.DOC: "L'aide a une rubrique Factures, mais ses captures d'écran ne sont plus à jour.",
}


def with_knowledge(role: Role, order: str) -> str:
    return f"{order}\n\nCe que tu sais du projet :\n{KNOWLEDGE[role]}"


def format_reports(mission: str, team: tuple[Manager | Worker, ...], reports: list[BaseModel]) -> str:
    lines = [f"[{member.role}] {report.model_dump_json()}" for member, report in zip(team, reports)]
    return f"Mission : {mission}\n\nRapports de ton équipe :\n" + "\n".join(lines)


def log(role: Role, output: BaseModel) -> None:
    print(f"\n[{role}] {type(output).__name__}\n{output.model_dump_json(indent=2)}")


async def run_worker(worker: Worker, mission: str) -> BaseModel:
    message = with_knowledge(worker.role, mission)
    report = await call(worker.agent, message)
    log(worker.role, report)

    return report


async def run_manager(manager: Manager, mission: str) -> BaseModel:
    orders = await call(manager.planner, mission)

    log(manager.role, orders)

    reports = await asyncio.gather(*(run(member, getattr(orders, member.role)) for member in manager.team))
    message = format_reports(mission, manager.team, reports)
    report = await call(manager.synthesizer, message)

    log(manager.role, report)

    return report


async def run(member: Manager | Worker, mission: str) -> BaseModel:
    match member:
        case Worker():
            return await run_worker(member, mission)
        case Manager():
            return await run_manager(member, mission)


async def main() -> None:
    await run(TREE, MISSION)


if __name__ == "__main__":
    asyncio.run(main())
