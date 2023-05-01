"""Description.

Test automatiques du bon format des données.
"""
from final.data import Donnees
import pytest

def test_Donnees():
    essai = Donnees(
        betaF= [75,90,225,2000,9,800,45],
    )
    isinstance(essai, Donnees)
    
def test_Donnees_problematiques():
    with pytest.raises(ValueError):
        Donnees(
        betaF= [90,225,2000,9,800,45],
    )
    with pytest.raises(ValueError):
        Donnees(
        betaF= [75,90,225,2000,9,800,45,18],
        )
    with pytest.raises(ValueError):
        Donnees(
        betaF= [75,90,225,-2000,9,800,45],
        )
    with pytest.raises(ValueError):
        Donnees(
        betaF= [75,'bla',225,2000,9,800,'blabla'],
        )
    with pytest.raises(ValueError):
        Donnees(
        betaF= [75.54,90.02,225,2000,9,800,45],
        )
