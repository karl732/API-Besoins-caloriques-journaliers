"""Description.

Librairie de résolution du problème complet.
"""
from .data import Donnees
import numpy as np
import scipy.optimize as opt

def resoud(donnees):
    # Extraire les données de l'objet Donnees
    nutriments = Donnees.nutriments
    aliments_index = Donnees.aliments_index
    contraintes_aliments = Donnees.contraintes_aliments
    contraintes_couts = Donnees.contraintes_couts
    besoins_journaliers = Donnees.besoins_journaliers
    
    # Extraire les valeurs associées à chaque aliment
    aliments = np.genfromtxt("Aliments.csv", delimiter=";", skip_header=1)
    aliments = aliments[:, 1:aliments_index+1].T
    
    # Formater les contraintes des nutriments
    A_ub = -aliments[:, :-1]
    b_ub = -np.array(contraintes_aliments)[:, 0]
    b_ub[b_ub == 0] = None
    
    # Formater les contraintes des coûts
    b_eq = contraintes_couts[0]
    
    # Formater les besoins journaliers
    #k = int
    betaF=np.array([75,90,225,9,800,45,-12]) 
    
    # Formater la fonction objectif(minimiser le coût)
    c = -aliments[:, -1]
    
    # Résoudre le problème d'optimisation linéaire
    result = opt.linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=betaF, b_eq=b_eq)
    
    # Formatter la solution
    solution = {}
    for i, nutriment in enumerate(nutriments):
        solution[nutriment] = round(
            np.sum(aliments[:, i] * result.x), 2
        )
    solution["coût"] = round(np.sum(aliments[:, -1] * result.x), 2)
    return solution