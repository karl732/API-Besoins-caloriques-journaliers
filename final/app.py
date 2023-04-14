"""Description.

Application ligne de commande pour la librairie du menu alimentaire.
"""
from .data import Donnees
from .lib_resolution import resoud

from serde.json import from_json, to_json
import typer
import numpy as np
import pandas as pd
from rich import print

app = typer.Typer()

@app.command()
class DietProblem:
    def __init__(self, A, z_ori, betaF):
        self.coeff = A[:-1]
        self.z_ori = z_ori
        self.betaF = betaF
        
        # Conversion des coefficients et du second membre en DataFrame Pandas
        self.coeff_df = pd.DataFrame(self.coeff, columns=self.get_ingredient_names())
        self.Marie_df = pd.DataFrame({"Marie": self.betaF}, index=self.get_nutriment_names())

@classmethod
def from_csv(cls, filename):
    # Lecture des données depuis un fichier CSV
    df = pd.read_csv(filename, sep=";", index_col=0)
    A = df.values.T
    z_ori = A[-1]
    betaF = np.array([75, 90, 225, 2000, 9, 800, 45])  # Valeurs pour Marie
    
    return cls(A, z_ori, betaF)

    def get_ingredient_names(self):
        return list(self.coeff_df.columns)

    def get_nutriment_names(self):
        return list(self.Marie_df.index)

if __name__ == "__main__":
    # Création du problème à partir du fichier Aliments.csv
    dp = DietProblem.from_csv("Aliments.csv")
    
    # Conversion du problème en graphe
    graph = problem_to_graph(dp)
    
    # Résolution du problème
    result = resoud(graph, dp.Marie)
    
    # Affichage du résultat
    print(result)