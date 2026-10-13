import asyncio

from pydantic import BaseModel

from llm import AgentConfig, Effort, Model, call
from prompts import BUG_PROMPT, FEATURE_PROMPT, ORCHESTRATOR_PROMPT, REFACTO_PROMPT
from schemas import BugReport, FeatureSpec, Issue, Plan, RefactoPlan, Task, WorkerType

ORCHESTRATOR = AgentConfig(Model.OPUS, Effort.HIGH, ORCHESTRATOR_PROMPT, Plan)

WORKERS = {
    WorkerType.BUG: AgentConfig(Model.OPUS, Effort.HIGH, BUG_PROMPT, BugReport),
    WorkerType.FEATURE: AgentConfig(Model.SONNET, Effort.MEDIUM, FEATURE_PROMPT, FeatureSpec),
    WorkerType.REFACTO: AgentConfig(Model.HAIKU, Effort.LOW, REFACTO_PROMPT, RefactoPlan),
}

ISSUES = [
    Issue(identifier=1, title="Le bouton 'Payer' ne répond plus sur Safari mobile"),
    Issue(identifier=2, title="Pouvoir exporter ses factures en CSV"),
    Issue(identifier=3, title="utils.py fait 1200 lignes, impossible à maintenir"),
    Issue(identifier=4, title="Crash au paiement sur iPhone depuis la v2.3"),
    Issue(identifier=5, title="Ajouter un mode sombre"),
]


def format_issues(issues: list[Issue]) -> str:
    return "\n".join(f"#{issue.identifier} {issue.title}" for issue in issues)


def issues_assigned_to(task: Task) -> list[Issue]:
    return [issue for issue in ISSUES if issue.identifier in task.issue_identifiers]


async def delegate(task: Task) -> BaseModel:
    issues = issues_assigned_to(task)
    message = f"{task.instructions}\n\nIssues :\n{format_issues(issues)}"
    return await call(WORKERS[task.worker], message)


async def main() -> None:
    plan = await call(ORCHESTRATOR, format_issues(ISSUES))
    results = await asyncio.gather(*(delegate(task) for task in plan.tasks))

    for task, result in zip(plan.tasks, results):
        print(f"\n[{task.worker}] issues {task.issue_identifiers}")
        print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
