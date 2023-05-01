"""Description.

Application ligne de commande pour la librairie du menu alimentaire.
"""

from final.data import Donnees
from final.lib_resolution import resoud
from serde.json import from_json, to_json
import typer
from rich import print

application = typer.Typer()

@application.command()
def essai(nom_fichier: str):
    essai = Donnees(
        betaF= [75,90,225,2000,9,800,45],
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