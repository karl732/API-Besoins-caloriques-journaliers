"""Description.

Application ligne de commande pour la librairie du menu alimentaire.
"""
from final.data import Donnees

from serde.json import from_json, to_json
import typer
from rich import print

from .data import DietProblem
from .conversion import problem_to_graph
from .resolution import solve_diet_problem

if __name__ == "__main__":
    # Création du problème à partir du fichier Aliments.csv
    dp = DietProblem.from_csv("Aliments.csv")
    
    # Conversion du problème en graphe
    graph = problem_to_graph(dp)
    
    # Résolution du problème
    result = solve_diet_problem(graph, dp.Marie)
    
    # Affichage du résultat
    print(result)

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