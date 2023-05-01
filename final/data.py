"""Description.

Classe Permettant de représenter les données d'un problème.

à part
## apports_nutritionnels: valeur en gramme ou en calorie associée à chaque aliments ##
"""

from serde import serde

@serde
class Donnees:
    """Représente les données du problème de résolution linprog.

    nutriments: liste de caractères
    besoins_journaliers: liste de couples nutriments / valeur associée
    aliments: liste d'index des aliments que l'on veut contraindre
    contraintes_aliments: liste de tuples valeurs seuils pour ce aliments
    contraintes_couts: liste de valeures seuils de prix de menu

    On vérifie après l'instanciation que le problème est "raisonnable":

    - les prix sont positifs
    - les nutriments des besoins journaliers sont existant

    La sérialisation est fait automatiquement vers json, yaml et toml via pyserde.

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

    >>> essai
    Donnees(personnages=['Berger', 'Loup', 'Mouton', 'Choux'], nb_places=2, rameurs=['Berger'],
    contraintes=[('Berger', ['Loup', 'Mouton']), ('Berger', ['Mouton', 'Choux'])])
    >>> from serde.json import to_json, from_json
    >>> code = to_json(essai)
    >>> code
    '{"personnages": ["Berger", "Loup", "Mouton", "Choux"], "nb_places": 2, "rameurs": ["Berger"],
    "contraintes": [["Berger", ["Loup", "Mouton"]], ["Berger", ["Mouton", "Choux"]]]}'
    >>> decode = from_json(Donnees, code)
    >>> decode
    Donnees(personnages=['Berger', 'Loup', 'Mouton', 'Choux'], nb_places=2, rameurs=['Berger'],
    contraintes=[('Berger', ['Loup', 'Mouton']), ('Berger', ['Mouton', 'Choux'])])
    """

    betaF: list[int]

    def __post_init__(self):
        for valeurs in self.betaF:
            if valeurs < 0:
                raise ValueError("Les besoins journaliers doivent être supérieure ou égal à zéro.")
        if len(self.betaF) != 7:
            raise ValueError("La valeur des 7 différents nutriments doit être fournie.")