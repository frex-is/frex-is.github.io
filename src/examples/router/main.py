import asyncio

from llm import AgentConfig, Effort, Model, call
from prompts import CLASSIFIER_PROMPT, COMPLEX_PROMPT, MEDIUM_PROMPT, SIMPLE_PROMPT
from schemas import DesignProposal, Diagnosis, Difficulty, QuickAnswer, RoutingDecision

CLASSIFIER = AgentConfig(Model.HAIKU, Effort.LOW, CLASSIFIER_PROMPT, RoutingDecision)
QUICK_ANSWERER = AgentConfig(Model.HAIKU, Effort.LOW, SIMPLE_PROMPT, QuickAnswer)
DEBUGGER = AgentConfig(Model.SONNET, Effort.MEDIUM, MEDIUM_PROMPT, Diagnosis)
ARCHITECT = AgentConfig(Model.OPUS, Effort.HIGH, COMPLEX_PROMPT, DesignProposal)

QUESTIONS = [
    "Comment inverser une liste en Python ?",
    "Pourquoi mon asyncio.gather bloque avec 1000 tâches qui font des requêtes HTTP ?",
    "Comment concevoir un rate limiter partagé entre plusieurs régions ?",
    "Mon code marche pas, pourquoi ?",
]


def move_to_unclear_questions(question: str) -> None:
    print(f"→ Transmise à un humain : {question}")


async def route(question: str) -> None:
    decision = await call(CLASSIFIER, question)
    print(f"\n[{decision.difficulty}] {question}")
    print(f"Raison : {decision.reason}")

    match decision.difficulty:
        case Difficulty.SIMPLE:
            response = await call(QUICK_ANSWERER, question)
        case Difficulty.MEDIUM:
            response = await call(DEBUGGER, question)
        case Difficulty.COMPLEX:
            response = await call(ARCHITECT, question)
        case Difficulty.UNCLEAR:
            move_to_unclear_questions(question)
            return

    print(response.model_dump_json(indent=2))


async def main() -> None:
    for question in QUESTIONS:
        await route(question)


if __name__ == "__main__":
    asyncio.run(main())
