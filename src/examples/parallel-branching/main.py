import asyncio
import re

from llm import AgentConfig, Effort, Model, call
from prompts import TRANSLATOR_PROMPT
from schemas import Language, Message, PlaceholderMismatch, Translation

TRANSLATOR = AgentConfig(Model.HAIKU, Effort.LOW, TRANSLATOR_PROMPT, Translation)

LANGUAGES = [Language.EN, Language.ES, Language.DE]

SOURCE = [
    Message(key="cart.empty", text="Votre panier est vide"),
    Message(key="cart.items", text="{count} articles dans votre panier"),
    Message(key="checkout.pay", text="Payer"),
]

PLACEHOLDER = re.compile(r"\{\w+\}")


def format_messages(messages: list[Message]) -> str:
    return "\n".join(f"{message.key} : {message.text}" for message in messages)


async def translate(language: Language) -> Translation:
    return await call(TRANSLATOR, f"Langue cible : {language}\n\n{format_messages(SOURCE)}")


def fan_in(results: list[Translation]) -> dict[Language, Translation]:
    return dict(zip(LANGUAGES, results))


def placeholders(text: str) -> set[str]:
    return set(PLACEHOLDER.findall(text))


def check_placeholders(catalog: dict[Language, Translation]) -> list[PlaceholderMismatch]:
    expected = {message.key: placeholders(message.text) for message in SOURCE}
    return [
        PlaceholderMismatch(
            language=language,
            key=message.key,
            expected=expected[message.key],
            found=placeholders(message.text),
        )
        for language, translation in catalog.items()
        for message in translation.messages
        if placeholders(message.text) != expected[message.key]
    ]


async def main() -> None:
    results = await asyncio.gather(*(translate(language) for language in LANGUAGES))
    catalog = fan_in(results)
    mismatches = check_placeholders(catalog)

    for language, translation in catalog.items():
        print(f"\n[{language}]")
        print(format_messages(translation.messages))

    print(f"\n[Placeholders] {len(mismatches)} erreur(s)")
    for mismatch in mismatches:
        print(f"{mismatch.language} · {mismatch.key} : attendu {mismatch.expected}, trouvé {mismatch.found}")


if __name__ == "__main__":
    asyncio.run(main())
