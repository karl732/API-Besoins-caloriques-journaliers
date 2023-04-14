"""Description.

Test automatiques de data.
"""
from final.data import Donnees
import pytest

def test_donnees():
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
    isinstance(essai, Donnees)
    
def test_donnees_problematiques():
    with pytest.raises(ValueError):
        Donnees(
            nutriments=["Kcal", "Protéines", "Glucides","Lipides",
                        "Fer", "Calcium", "Fibre"],
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
    with pytest.raises(ValueError):
        Donnees(
            nutriments=["Kcal", "Protéines", "Glucides","Lipides",
                        "Fer", "Calcium", "Fibre"],
            aliments_index=25,
            contraintes_nutriments=[(0, 5)],
            contraintes_couts=[2,4,6,8,10],
            besoins_journaliers=[
        ("Kcal", 2000),
        ("Protéines", 75),
        ("Glucides", 225),
        ("Lipides", 90),
        ("Fer", 9),
        ("Fibre", 45),
        ],
            )
    with pytest.raises(ValueError):
        Donnees(
            nutriments=["Kcal", "Protéines", "Glucides","Lipides",
                        "Fer", "Calcium", "Fibre"],
            aliments_index=25,
            contraintes_nutriments=[(0, 0)],
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
    with pytest.raises(ValueError):
        Donnees(
            nutriments=["Kcal", "Protéines", "Glucides","Lipides",
                        "Fer", "Calcium", "Fibre"],
            aliments_index=25,
            contraintes_nutriments=[(0, 5)],
            contraintes_couts=[],
            besoins_journaliers=[
        ("Kcal", 2100),
        ("Protéines", 65),
        ("Glucides", 295),
        ("Lipides", 80),
        ("Fer", 11),
        ("Fibre", 75),
        ],
            )
