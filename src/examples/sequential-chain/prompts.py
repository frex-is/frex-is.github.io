TRIAGE_PROMPT = """\
Tu tries les commits d'une nouvelle version d'application. Pour chaque commit, choisis une catégorie :
- feature : nouvelle fonctionnalité visible par l'utilisateur ;
- fix : correction d'un problème visible par l'utilisateur ;
- internal : refactoring, CI, outillage… invisible pour l'utilisateur.

Résume ensuite en une phrase ce qui change pour l'utilisateur, sans jargon technique.
"""

RELEASE_NOTES_PROMPT = """\
Tu rédiges les release notes d'une application à partir d'une liste de changements triés.

- Ignore les changements internal : ils n'intéressent pas les utilisateurs.
- Écris une ligne courte par changement, au présent, centrée sur le bénéfice pour l'utilisateur.
- N'ajoute aucun changement absent de la liste.
"""

ANNOUNCEMENT_PROMPT = """\
Tu es community manager. À partir des release notes, écris une annonce courte (2 ou 3 phrases) \
pour présenter la nouvelle version aux utilisateurs.

Ne mentionne que ce qui figure dans les release notes.
"""
