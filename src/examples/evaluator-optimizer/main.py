import asyncio

from llm import AgentConfig, Effort, Model, call
from prompts import GENERATOR_PROMPT, JUDGE_PROMPT, SPEC
from schemas import CartTestCase, CustomerTier, GeneratedCode, IntentReview

MAX_REVISIONS = 3

GENERATOR = AgentConfig(Model.HAIKU, Effort.LOW, GENERATOR_PROMPT, GeneratedCode)
JUDGE = AgentConfig(Model.SONNET, Effort.MEDIUM, JUDGE_PROMPT, IntentReview)

TEST_CASES = [
    CartTestCase("sous le seuil : port payant", [20.0, 10.0], CustomerTier.STANDARD, 34.90),
    CartTestCase("pile 50 € : port offert", [30.0, 20.0], CustomerTier.STANDARD, 50.00),
    CartTestCase("55 € remisés à 49,50 € : port payant", [30.0, 25.0], CustomerTier.LOYAL, 54.40),
    CartTestCase("60 € remisés à 54 € : port offert", [60.0], CustomerTier.LOYAL, 54.00),
    CartTestCase("panier vide : port payant", [], CustomerTier.STANDARD, 4.90),
]


def run_tests(code: str) -> list[str]:
    namespace = {"CustomerTier": CustomerTier}

    try:
        exec(code, namespace)
        cart_total = namespace["cart_total"]
    except Exception as error:
        return [f"le code ne s'exécute pas : {error!r}"]

    failures = []
    
    for case in TEST_CASES:
        total = cart_total(case.prices, case.customer_tier)

        if total != case.expected_total:
            failures.append(f"{case.description} → attendu {case.expected_total}, obtenu {total}")
    
    return failures


async def judge_intent(code: str) -> list[str]:
    review = await call(JUDGE, f"{SPEC}\nCode à relire :\n{code}")
    return [f"`{issue.subject}` : {issue.problem} → {issue.suggestion}" for issue in review.issues]


def revision_request(code: str, issues: list[str]) -> str:
    defects = "\n".join(f"- {issue}" for issue in issues)
    return f"{SPEC}\nTa version précédente :\n{code}\n\nDéfauts à corriger :\n{defects}"


async def main() -> None:
    specification = SPEC

    for revision in range(1, MAX_REVISIONS + 1):
        draft = await call(GENERATOR, specification)
        print(f"── Révision {revision} ──\n{draft.code}\n")

        issues = run_tests(draft.code)
        if not issues:
            print(f"Tests → ✅ {len(TEST_CASES)}/{len(TEST_CASES)}")
            issues = await judge_intent(draft.code)

        if not issues:
            print(f"Juge → ✅\nLivré en {revision} révision(s).")
            break

        print("\n".join(f"❌ {issue}" for issue in issues) + "\n")
        specification = revision_request(draft.code, issues)
    else:
        print(f"Budget de {MAX_REVISIONS} révisions épuisé.")


if __name__ == "__main__":
    asyncio.run(main())
