"""Description.

Application ligne de commande pour la librairie du menu alimentaire.
"""
from .data import Donnees
from .resolution import solve_diet_problem
from serde.json import from_json, to_json
import typer
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
    
    
if __name__ == "__main__":
    application()