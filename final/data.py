"""Description.

Classe Permettant de représenter les données d'un problème.

à part
## apports_nutritionnels: valeur en gramme ou en calorie associée à chaque aliments ##
"""

from serde import serde
import pandas as pd
import numpy as np

@serde
class Donnees:
    """Représente les données du problème du menu dietétique.

    nutriments: liste de caractères
    besoins_journaliers: liste de couples nutriments / valeur associée
    aliments: liste d'index des aliments que l'on veut contraindre
    contraintes_aliments: liste de tuples valeurs seuils pour ce aliments
    contraintes_couts: liste de valeures seuils de prix de menu

    On vérifie après l'instanciation que le problème est "raisonnable":

    - les prix sont positifs
    - les nutriments des besoins journaliers sont existant

    La sérialisation est fait automatiquement vers json, yaml et toml via pyserde.

- Kcal : 2000kcal (F)
- Protéines : 75g (F)
- Glucides : 225g (F)
- Lipides : 90g (F)
- Fer : 9mg (F) 
- Calcium : 0.8g (F)
- Fibre : 45g (F)

    Exemple:
    >>> essai = Donnees(
    ...     nutriments=["Kcal", "Protéines", "Glucides", "Lipides", "Fer", "Calcium", "Fibre"],
    ...     aliments_index=25,
    ...     contraintes_nutriments=[(0, 5)],
    ...     contraintes_couts=[12],
    ...     besoins_journaliers=[
    ...         ("Kcal", 2000),
    ...         ("Protéines", 75),
    ...         ("Glucides", 225),
    ...         ("Lipides", 90),
    ...         ("Fer", 9),
    ...         ("Fibre", 45),
    ...     ],
    ... )
    
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
    aliments_index: int
    contraintes_aliments: tuple[int, int]
    contraintes_couts: list[int]
    besoins_journaliers: list[tuple[str, int]]

    def __post_init__(self):
        if self.aliments_index < 0:
            raise ValueError("L'indice de l'aliment positif ou nul")
        for mini, maxi in self.contraintes_aliments:
            if mini < 0:
                raise ValueError(
                    "La valeure minimale doit être positive ou supérieure à zéro")
            if maxi < mini:
                raise ValueError(
                    "La valeure max doit être supérieure à la valeure min")
        if self.contraintes_couts <= 0:
            raise ValueError("Le prix du menu doit être positif.")
        for nutriment, apports in self.besoins_journaliers:
            if nutriment not in self.nutriments:
                raise ValueError(
                    "Les nutriments doivent être des nutriments existants."
                )
            for apport in apports:
                if apport <= 0:
                    raise ValueError(
                        "Le besoin de nutriments doit être positif")

class DietProblem:
    def __init__(self, A, z_ori, Marie):
        self.coeff = A[:-1]
        self.z_ori = z_ori
        self.Marie = Marie
        
        # Conversion des coefficients et du second membre en DataFrame Pandas
        self.coeff_df = pd.DataFrame(self.coeff, columns=self.get_ingredient_names())
        self.Marie_df = pd.DataFrame({"Marie": self.Marie}, index=self.get_nutriment_names())

    @classmethod
    def from_csv(cls, filename):
        # Lecture des données depuis un fichier CSV
        df = pd.read_csv(filename, sep=";", index_col=0)
        A = df.values.T
        z_ori = A[-1]
        Marie = np.array([75, 90, 225, 2000, 9, 800, 45])  # Valeurs pour Marie
        
        return cls(A, z_ori, Marie)

    def get_ingredient_names(self):
        return list(self.coeff_df.columns)

    def get_nutriment_names(self):
        return list(self.Marie_df.index)