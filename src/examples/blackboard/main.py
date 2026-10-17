import asyncio

from pydantic import BaseModel

from llm import AgentConfig, Effort, Model, call
from prompts import BACKEND_PROMPT, FRONTEND_PROMPT, REPORTER_PROMPT, VERIFIER_PROMPT
from schemas import AgentName, Board, Conclusion, Entry, Hypothesis, Status, Verdict

MAX_STEPS = 10

SYMPTOM = "Crash au paiement sur iPhone depuis la v2.3"

AGENTS = {
    AgentName.FRONTEND: AgentConfig(Model.HAIKU, Effort.LOW, FRONTEND_PROMPT, Hypothesis),
    AgentName.BACKEND: AgentConfig(Model.HAIKU, Effort.LOW, BACKEND_PROMPT, Hypothesis),
    AgentName.VERIFIER: AgentConfig(Model.SONNET, Effort.MEDIUM, VERIFIER_PROMPT, Verdict),
    AgentName.REPORTER: AgentConfig(Model.HAIKU, Effort.LOW, REPORTER_PROMPT, Conclusion),
}

KNOWLEDGE = {
    AgentName.FRONTEND: "v2.3 : mise à jour de Stripe.js et nouveau bouton Apple Pay sur la page de paiement.",
    AgentName.BACKEND: "v2.3 : le webhook de paiement convertit les montants Apple Pay (« 19.99 ») en centimes avec float(amount) * 100.",
}

EVIDENCE = """\
[safari-ios] Stripe.js 4.2 chargé, bouton Apple Pay affiché, paiement autorisé par Apple
[api] POST /payments/webhook 422 « amount must be an integer » (amount=1998.9999999999998)
[api] POST /payments/webhook 200 (carte, amount=1999)
"""


def open_hypothesis(board: Board) -> Entry | None:
    return next((entry for entry in board.hypotheses if entry.status == Status.OPEN), None)


def has_confirmed(board: Board) -> bool:
    return any(entry.status == Status.CONFIRMED for entry in board.hypotheses)


def has_proposed(board: Board, author: AgentName) -> bool:
    return any(entry.author == author for entry in board.hypotheses)


def reporter_ready(board: Board) -> bool:
    return has_confirmed(board) and board.conclusion is None


def verifier_ready(board: Board) -> bool:
    return open_hypothesis(board) is not None


def frontend_ready(board: Board) -> bool:
    return open_hypothesis(board) is None and not has_confirmed(board) and not has_proposed(board, AgentName.FRONTEND)


def backend_ready(board: Board) -> bool:
    return open_hypothesis(board) is None and not has_confirmed(board) and not has_proposed(board, AgentName.BACKEND)


CONTROLLER_PRIORITY_CHECKS = {
    AgentName.REPORTER: reporter_ready,
    AgentName.VERIFIER: verifier_ready,
    AgentName.FRONTEND: frontend_ready,
    AgentName.BACKEND: backend_ready,
}


def message(name: AgentName, board: Board) -> str:
    sections = [f"Tableau :\n{board.model_dump_json(indent=2)}"]

    if name in KNOWLEDGE:
        sections.append(f"Ce que tu sais de la v2.3 :\n{KNOWLEDGE[name]}")

    if name == AgentName.VERIFIER:
        sections.append(f"Logs de production :\n{EVIDENCE}")

    return "\n\n".join(sections)


def write(board: Board, name: AgentName, output: BaseModel) -> None:
    match output:
        case Hypothesis():
            entry = Entry(identifier=len(board.hypotheses) + 1, author=name, statement=output.statement)
            board.hypotheses.append(entry)
        case Verdict():
            entry = open_hypothesis(board)
            entry.status = output.status
            entry.evidence = output.evidence
        case Conclusion():
            board.conclusion = f"{output.root_cause} Correction : {output.fix}"

    board.version += 1


async def main() -> None:
    board = Board(symptom=SYMPTOM)
    print(f"v{board.version} [symptôme] {board.symptom}\n")

    for _ in range(MAX_STEPS):
        name = next((name for name, ready in CONTROLLER_PRIORITY_CHECKS.items() if ready(board)), None)

        if name is None:
            print("Enquête bloquée : plus aucun agent n'est prêt")
            break

        output = await call(AGENTS[name], message(name, board))
        write(board, name, output)
        print(f"v{board.version} [{name}] {output.model_dump_json()}\n")

        if board.conclusion:
            print(f"Tableau final :\n{board.model_dump_json(indent=2)}")
            break
    else:
        print(f"Pas de conclusion après {MAX_STEPS} étapes")


if __name__ == "__main__":
    asyncio.run(main())
