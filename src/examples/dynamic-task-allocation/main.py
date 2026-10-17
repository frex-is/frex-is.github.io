import asyncio
from dataclasses import dataclass

from llm import AgentConfig, Effort, Model, call
from prompts import BID_PROMPT, SOLVE_PROMPT
from schemas import AgentName, Bid, BidSheet, Issue, Resolution


@dataclass(frozen=True)
class Agent:
    model: Model
    effort: Effort
    hourly_rate: int
    capacity: int


AGENTS = {
    AgentName.JUNIOR: Agent(Model.HAIKU, Effort.LOW, hourly_rate=1, capacity=2),
    AgentName.SENIOR: Agent(Model.SONNET, Effort.MEDIUM, hourly_rate=3, capacity=1),
    AgentName.EXPERT: Agent(Model.OPUS, Effort.HIGH, hourly_rate=10, capacity=1),
}

ISSUES = [
    Issue(identifier=1, title="Le bouton 'Payer' ne répond plus sur Safari mobile"),
    Issue(identifier=2, title="Pouvoir exporter ses factures en CSV"),
    Issue(identifier=3, title="utils.py fait 1200 lignes, impossible à maintenir"),
    Issue(identifier=4, title="Ajouter un mode sombre"),
]


def format_issues(issues: list[Issue]) -> str:
    return "\n".join(f"#{issue.identifier} {issue.title}" for issue in issues)


def bidder(name: AgentName) -> AgentConfig:
    agent = AGENTS[name]
    bid_system = BID_PROMPT.format(level=name, hourly_rate=agent.hourly_rate)

    return AgentConfig(agent.model, agent.effort, bid_system, BidSheet)


def solver(name: AgentName) -> AgentConfig:
    agent = AGENTS[name]
    solve_system = SOLVE_PROMPT.format(level=name)

    return AgentConfig(agent.model, agent.effort, solve_system, Resolution)


def lowest_price_first(offer: tuple[AgentName, Bid]) -> float:
    _, bid = offer
    return bid.price


def by_issue_then_cheapest(offer: tuple[AgentName, Bid]) -> tuple[int, float]:
    _, bid = offer
    return bid.issue_identifier, bid.price


async def collect_bids() -> list[tuple[AgentName, Bid]]:
    sheets = await asyncio.gather(*(call(bidder(name), format_issues(ISSUES)) for name in AGENTS))

    return [
        (name, bid) 
        for name, sheet in zip(AGENTS, sheets) 
        for bid in sheet.bids
    ]


def allocate(bids: list[tuple[AgentName, Bid]]) -> dict[int, AgentName]:
    assignments = {}
    remaining_capacity = {
        name: agent.capacity 
        for name, agent in AGENTS.items()
    }

    for name, bid in sorted(bids, key=lowest_price_first):
        if bid.issue_identifier not in assignments and remaining_capacity[name] > 0:
            assignments[bid.issue_identifier] = name
            remaining_capacity[name] -= 1
    
    return assignments


async def main() -> None:
    bids = await collect_bids()
    
    for name, bid in sorted(bids, key=by_issue_then_cheapest):
        print(f"#{bid.issue_identifier} [{name}] {bid.price:>6.1f}  {bid.justification}")

    assignments = allocate(bids)
    results = await asyncio.gather(*(call(solver(assignments[issue.identifier]), format_issues([issue])) for issue in ISSUES))

    for issue, result in zip(ISSUES, results):
        print(f"\n[{assignments[issue.identifier]}] #{issue.identifier} {issue.title}")
        print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
