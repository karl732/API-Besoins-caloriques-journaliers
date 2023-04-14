"""Description.

Application ligne de commande pour la librairie du menu alimentaire.
"""
from .data import Donnees
from .resolution import solve_diet_problem
from serde.json import from_json, to_json
import typer
import numpy as np
import pandas as pd
from rich import print

app = typer.Typer()

@app.command()
def essai(nom_fichier: str):
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
    
    with open(nom_fichier, "w") as fichier:
        fichier.write(code)
        
        
@application.command()
def calcule(nom_fichier: str):
    with open(nom_fichier, "r") as fichier:
        code = fichier.read()
        
    donnees = from_json(Donnees, code)
    solution = resoud(donnees)
    print(solution)
    
    
    # Création du problème à partir du fichier Aliments.csv
    dp = DietProblem.from_csv("Aliments.csv")
    
    # Conversion du problème en graphe
    graph = problem_to_graph(dp)
    
    # Résolution du problème
    result = solve_diet_problem(graph, dp.Marie)
    
    # Affichage du résultat
    print(result)
    
if __name__ == "__main__":
    application()
    
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