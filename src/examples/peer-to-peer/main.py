import asyncio

from llm import AgentConfig, Effort, Model, call
from prompts import CLIENT_PROMPT, FREELANCE_PROMPT, SENIOR_PROMPT
from schemas import ClientMessage, FreelanceMessage, NegotiatorMessage, Peer, SeniorMessage, Status

MAX_TURNS = 10

BRIEF = "Besoin : pouvoir exporter ses factures en CSV. Rédige ta demande au freelance."

PEERS = {
    Peer.CLIENT: AgentConfig(
        Model.HAIKU, Effort.LOW,
        CLIENT_PROMPT.format(name=Peer.CLIENT, budget=3000, deadline=15),
        ClientMessage,
    ),
    Peer.FREELANCE: AgentConfig(
        Model.HAIKU, Effort.LOW,
        FREELANCE_PROMPT.format(name=Peer.FREELANCE, floor_price=2000, available_in=5),
        FreelanceMessage,
    ),
    Peer.SENIOR: AgentConfig(
        Model.SONNET, Effort.MEDIUM,
        SENIOR_PROMPT.format(name=Peer.SENIOR),
        SeniorMessage,
    ),
}


def deliver(histories: dict[Peer, list[str]], sender: Peer, receiver: Peer, content: str) -> None:
    line = f"[{sender} -> {receiver}] {content}"
    histories[sender].append(line)
    histories[receiver].append(line)
    print(f"{line}\n")


async def main() -> None:
    histories = {peer: [] for peer in Peer}

    sender = Peer.CLIENT
    reply = await call(PEERS[sender], BRIEF)

    for _ in range(MAX_TURNS):
        receiver = Peer(reply.to)

        deliver(histories, sender, receiver, reply.content)

        negotiation_closed = isinstance(reply, NegotiatorMessage) and reply.status != Status.NEGOTIATING

        if negotiation_closed:
            print(f"Négociation close : {reply.status}")
            break

        sender = receiver
        reply = await call(PEERS[sender], "\n".join(histories[sender]))
    else:
        print(f"Pas d'accord après {MAX_TURNS} tours")


if __name__ == "__main__":
    asyncio.run(main())
