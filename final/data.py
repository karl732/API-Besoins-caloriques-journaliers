"""Description.

Classe Permettant de représenter les données d'un problème.

à part
## apports_nutritionnels: valeur en gramme ou en calorie associée à chaque aliments ##
"""

from serde import serde
from rich import print

@serde
class Donnees:
    """Représente les données du problème de résolution d'optimisation alimentaire.

    betaF: liste des besoins journaliers pour les 7 nutriments principaux
           [Kcal, Protéines, Glucides, Lipides, Fer, Calcium, Fibres]
    
    La sérialisation est fait automatiquement vers json, yaml et toml via pyserde.

    Exemple:
    >>> essai = Donnees(betaF=[2000, 75, 225, 90, 9, 800, 45])
    >>> from serde.json import to_json, from_json
    >>> code = to_json(essai)
    >>> decode = from_json(Donnees, code)
    """

    betaF: list[int]

    def __post_init__(self):
        """Validation des données après initialisation."""
        if len(self.betaF) != 7:
            raise ValueError("La valeur des 7 différents nutriments doit être fournie.")
        
        nutriments = ["Kcal", "Protéines", "Glucides", "Lipides", "Fer", "Calcium", "Fibres"]
        
        for i, valeur in enumerate(self.betaF):
            if not isinstance(valeur, (int, float)) or valeur < 0:
                raise ValueError(f"Le besoin journalier pour {nutriments[i]} doit être un nombre positif.")