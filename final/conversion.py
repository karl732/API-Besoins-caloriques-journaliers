"""Description.

Fonctionnalités de conversion du problème brute vers un graphe.
"""

from .data import Donnees
from serde.json import to_json, from_json

essai = Donnees(
    nutriments=["Kcal", "Protéines", "Glucides",
                "Lipides", "Fer", "Calcium", "Fibre"],
    aliments_index=25,
    contraintes_nutriments=[(0, 5)],
    contraintes_couts=[12],
    besoins_journaliers=[
        ("Kcal", 2000),
        ("Protéines", 75),
        ("Glucides", 225),
        ("Lipides", 90),
        ("Fer", 9),
        ("Fibre", 45),
    ],
)

code = to_json(essai)
code