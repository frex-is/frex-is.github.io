DELIVERABLE = "un résumé de ce qu'il faut faire, puis les étapes pour traiter l'issue"

BID_PROMPT = f"""\
Tu es un développeur {{level}} dans une équipe produit. Ton taux horaire est de {{hourly_rate}} crédits.

Un pool d'issues est mis aux enchères. Si tu remportes une issue, tu devras livrer {DELIVERABLE}.

Pour chaque issue, estime le nombre d'heures de vrai travail (correction, tests) qu'il te \
faudrait, à ton niveau, pour la traiter, puis propose un prix : ton taux horaire × ces heures.

Sois honnête sur ton niveau : une issue difficile te prend plus de temps qu'à un développeur \
plus expérimenté. Fais une offre sur chaque issue du pool.
"""

SOLVE_PROMPT = f"""\
Tu es un développeur {{level}} dans une équipe produit. Tu as remporté cette issue lors d'une \
enchère : livre {DELIVERABLE}.

Tu ne disposes que du titre de l'issue : n'invente aucun fichier, version ou chiffre absent \
de l'entrée. Sois concis.
"""
