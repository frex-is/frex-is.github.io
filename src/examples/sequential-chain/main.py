import asyncio

from llm import AgentConfig, Effort, Model, call
from prompts import ANNOUNCEMENT_PROMPT, RELEASE_NOTES_PROMPT, TRIAGE_PROMPT
from schemas import Announcement, Commit, ReleaseNotes, Triage

TRIAGE = AgentConfig(Model.HAIKU, Effort.LOW, TRIAGE_PROMPT, Triage)
RELEASE_NOTES = AgentConfig(Model.SONNET, Effort.MEDIUM, RELEASE_NOTES_PROMPT, ReleaseNotes)
ANNOUNCEMENT = AgentConfig(Model.HAIKU, Effort.LOW, ANNOUNCEMENT_PROMPT, Announcement)

COMMITS = [
    Commit(sha="a1b2", message="✨ ajout de l'export CSV des factures"),
    Commit(sha="c3d4", message="🐛 fix crash au paiement sur Safari"),
    Commit(sha="e5f6", message="♻️ découpage de utils.py"),
    Commit(sha="g7h8", message="💄 ajout du mode sombre"),
]


def format_commits(commits: list[Commit]) -> str:
    return "\n".join(f"{commit.sha} {commit.message}" for commit in commits)


async def main() -> None:
    triage = await call(TRIAGE, format_commits(COMMITS))
    release_notes = await call(RELEASE_NOTES, triage.model_dump_json(indent=2))
    announcement = await call(ANNOUNCEMENT, release_notes.model_dump_json(indent=2))

    for step, output in [("Tri", triage), ("Release notes", release_notes), ("Annonce", announcement)]:
        print(f"\n[{step}]")
        print(output.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
