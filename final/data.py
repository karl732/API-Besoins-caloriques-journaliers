"""Description.

Classe Permettant de représenter les données d'un problème.

à part
## apports_nutritionnels: valeur en gramme ou en calorie associée à chaque aliments ##
"""

from serde import serde

@serde
class Donnees:
    """Représente les données du problème du menu dietétique.

    nutriments: liste de caractères
    besoins_journaliers: liste de couples nutriments / valeur associée
    contraintes_nutriment: liste de valeurs seuils de nutriments
    contraintes_couts: liste de valeures seuils de prix de menu

    On vérifie après l'instanciation que le problème est "raisonnable":
    
    - les prix sont positifs
    - les nutriments des besoins journaliers sont existant

    La sérialisation est fait automatiquement vers json, yaml et toml via pyserde.

    Exemple:
    >>> essai = Donnees(
    ...     personnages=["Berger", "Loup", "Mouton", "Choux"],
    ...     nb_places=2,
    ...     rameurs=["Berger"],
    ...     contraintes=[
    ...         ("Berger", ["Loup", "Mouton"]),
    ...         ("Berger", ["Mouton", "Choux"]),
    ...     ],
    ... )
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

    nutriments: list[str]
    contraintes_nutriment: list[int]
    contraintes_couts: list[int]
    besoins_journaliers: list[tuple[str, int]]

    def __post_init__(self):
        if self.contraintes_couts <= 0:
            raise ValueError("Le prix du menu doit être positif.")
        if self.contraintes_nutriment <= 0:
            raise ValueError("Les besoins journaliers doivent être positif.")
        for nutriment, apports in self.besoins_journaliers:
            if nutriment not in self.nutriments:
                raise ValueError(
                    "Les nutriments doivent être des nutriments existants."
                    )
            for apport in apports:
                if apport <= 0:
                    raise ValueError(
                        "Le besoin de nutriments doit être positif")