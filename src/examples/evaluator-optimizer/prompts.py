SPEC = """\
Écris une fonction `cart_total(prices: list[float], customer_tier: CustomerTier) -> float`.

- Les clients fidèles ont 10 % de remise sur le sous-total.
- Les frais de port sont de 4,90 €, offerts dès 50 € d'achat (après remise).
- Le total est arrondi au centime.

L'enum suivante est déjà importée, ne la redéfinis pas :

class CustomerTier(StrEnum):
    STANDARD = "standard"
    LOYAL = "loyal"
"""

GENERATOR_PROMPT = """\
Tu es développeur Python. Tu écris le code demandé par la spec : rends le module complet, \
sans import inutile ni exemple d'utilisation.

Si ton message contient une version précédente et des défauts, corrige chacun d'eux \
sans casser le reste.
"""

JUDGE_PROMPT = """\
Tu relis du code Python qui passe déjà tous ses tests. Ne juge ni la correction ni le style \
général : juge uniquement si les noms portent l'intention métier de la spec.

Grille :
1. chaque valeur métier (taux, seuil, montant) est une constante nommée ;
2. chaque variable dit quelle grandeur métier elle contient ;
3. les noms reprennent le vocabulaire de la spec.

Ne signale que ce qui enfreint la grille, pas tes préférences. Rends une liste vide si \
la grille est respectée.
"""
