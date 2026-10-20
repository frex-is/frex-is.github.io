import asyncio
from collections import Counter

from llm import AgentConfig, Effort, Model, call
from prompts import NEUTRAL_PROMPT, PRODUCT_PROMPT, SRE_PROMPT, SUPPORT_PROMPT
from schemas import Outcome, Ticket, Verdict, Vote, Voter

MIN_AGREEING_VOTES = 3

VOTERS = {
    Voter.SUPPORT: AgentConfig(Model.HAIKU, Effort.LOW, SUPPORT_PROMPT, Vote),
    Voter.SRE: AgentConfig(Model.HAIKU, Effort.LOW, SRE_PROMPT, Vote),
    Voter.PRODUCT: AgentConfig(Model.HAIKU, Effort.LOW, PRODUCT_PROMPT, Vote),
    Voter.NEUTRAL: AgentConfig(Model.SONNET, Effort.MEDIUM, NEUTRAL_PROMPT, Vote),
}

TICKETS = [
    Ticket(501, "Le paiement échoue pour tous les clients depuis 14h",
           "Toutes les tentatives de paiement renvoient « erreur inconnue ». Aucune commande validée depuis 40 minutes."),
    Ticket(502, "L'export CSV des factures est très lent sur les gros comptes",
           "Au-delà de 5 000 factures, l'export met environ 40 s au lieu de 5 s. Le fichier finit par arriver."),
    Ticket(503, "Un client grand compte ne peut plus télécharger ses factures 2023",
           "Un seul compte touché, mais il représente 20 % du chiffre d'affaires. Le support lui envoie les PDF par mail en attendant."),
]


async def collect_votes(ticket: Ticket) -> dict[Voter, Vote]:
    message = f"#{ticket.number} {ticket.title}\n{ticket.description}"
    votes = await asyncio.gather(*(call(agent, message) for agent in VOTERS.values()))
    return dict(zip(VOTERS, votes))


def count_votes(votes: list[Vote]) -> Verdict:
    leading_priority, agreeing_votes = Counter(vote.priority for vote in votes).most_common(1)[0]
    outcome = Outcome.RETAINED if agreeing_votes >= MIN_AGREEING_VOTES else Outcome.ESCALATED
    return Verdict(leading_priority, agreeing_votes, outcome)


async def main() -> None:
    for ticket in TICKETS:
        print(f"── #{ticket.number} {ticket.title} ──")
        votes = await collect_votes(ticket)

        for voter, vote in votes.items():
            print(f"  {voter:<8} {vote.priority}  « {vote.reason} »")

        verdict = count_votes(list(votes.values()))
        score = f"{verdict.leading_priority} {verdict.agreeing_votes}/{len(VOTERS)}"

        if verdict.outcome is Outcome.RETAINED:
            print(f"  → ✅ {score}\n")
        else:
            print(f"  → ⚠️ pas assez de votes d'accord ({score}) → escalade au lead\n")


if __name__ == "__main__":
    asyncio.run(main())
