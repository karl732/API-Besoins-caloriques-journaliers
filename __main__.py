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
def exemple(nom_fichier: str):
    """Génère un fichier d'exemple avec des données par défaut."""
    exemple_donnees = Donnees(
        betaF=[2000, 75, 225, 90, 9, 800, 45],  # Kcal, Protéines, Glucides, Lipides, Fer, Calcium, Fibres
    )
    
    code = to_json(exemple_donnees)
    
    with open(nom_fichier, "w") as fichier:
        fichier.write(code)
    
    print(f"[green]Fichier d'exemple généré : {nom_fichier}[/green]")


@application.command()
def calcule(nom_fichier: str):
    """Résout le problème d'optimisation à partir du fichier de données."""
    try:
        with open(nom_fichier, "r") as fichier:
            code = fichier.read()
            
        donnees = from_json(Donnees, code)
        solution = resoud(donnees)
        
        print("[bold blue]Résultat de l'optimisation :[/bold blue]")
        print(solution[0])
        print(solution[1])
        
    except FileNotFoundError:
        print(f"[red]Erreur : Le fichier {nom_fichier} n'existe pas.[/red]")
    except Exception as e:
        print(f"[red]Erreur lors du calcul : {str(e)}[/red]")
    
    
if __name__ == "__main__":
    application()