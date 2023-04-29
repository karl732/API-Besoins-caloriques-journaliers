"""Description.

Librairie de résolution du problème complet.
"""
import numpy as np
import pandas as pd
import scipy.optimize as so

from .data import Donnees

# Extraire les valeurs associées à chaque aliment
Al = pd.read_csv('./Aliments.csv', sep=';', index_col=0)
aliments = np.array(Al).T


def apports(RESULT):
    """La fonction apport permet de calculer les apports de chaque aliments nécessaire pour réaliser l'optimum.

    Args:
        RESULT (_OptimizeResult_): scipy.optimize.OptimizeResult est un objet scipy optimise,
        qui retourne plusieurs éléments en fonction de la réussite de l'optimisation, 
        comme {x} la valeur réalisant l'optimum, {fun} la valeur que prend notre fonction à l'optimum etc.

    Returns:
        REPAS(_pd.dataframe_): dataframe pandas comprenant les quantités 
        de chaque aliments non nul pour réaliser l'optimum, ainsi que le détails
        de ces quantité en valeur our chaque nutriment.
    """
    A = RESULT.x
    u, = A.nonzero()
    REST = Al.iloc[u, :]
    QTE = pd.DataFrame(
        {'Quantités en g': 100*A[A.nonzero()]}).set_index(Al.iloc[u, :].index)
    BILAN = pd.DataFrame(
        (np.array(REST).T*A[A.nonzero()]).T).set_index(QTE.index)
    REPAS = pd.concat([QTE, BILAN], axis=1)
    REPAS = REPAS.append([REPAS.sum()])
    Namescol = ['Quantité (en g)']+list(Al.columns)
    Namescol[-1] = 'Prix (en €)'
    REPAS.columns = Namescol
    Namesrow = list(QTE.index)
    Namesrow.append('Apports du repas')
    REPAS.index = Namesrow
    return REPAS


def rename_aliment(old_name):
    """
    Fonction qui permet d'enlever le type de chaque aliment de sorte à fournir un résultat plus clair.
    """
    new_name = old_name.replace("Lait – ", "")
    new_name = new_name.replace("Viande – ", "")
    new_name = new_name.replace("Poisson – ", "")
    new_name = new_name.replace("Légume – ", "")
    new_name = new_name.replace("Base – ", "")
    return new_name


def resoud(donnees: Donnees):
    """_summary_

afin de vérifier si l'optimisation est un succès : OptimizeResult.status
    Args:
        donnees (_str_): fichier codé en .json avec les données du problème.

    Returns:
        phrase(_str_): phrase synthétisant le résultat de l'optimisation, en fournissant
        les aliments et les quantités réalisant l'optimum, le prix ainsi que les calorie du repas optimal.
    """
    # Extraire les données de l'objet Donnees
    # nutriments = Donnees.nutriments
    # aliments_index = Donnees.aliments_index
    # contraintes_aliments = Donnees.contraintes_aliments
    # contraintes_couts = Donnees.contraintes_couts
    # besoins_journaliers = Donnees.besoins_journaliers

    # Formater les contraintes des aliments
    coeff = aliments[:, :-1]
    bdns = [(0, None) for k in range(41)]
    bdns[25] = (0, 5)

    # Formater les contraintes des coûts
    # b_eq = contraintes_couts[0]

    # Formater les besoins journaliers
    # k = int
    betaF = np.array([75,90,225,2000,9,800,45])

    # Formater la fonction objectif(minimiser le coût)
    c = -aliments[:, -1]

    # Résoudre le problème d'optimisation linéaire
    RESULT = so.linprog(c, A_ub=-coeff, b_ub=-betaF, method='simplex')
    # Formatter la solution
    A = RESULT.x
    u, = A.nonzero()
    Qt = A[u]
    Phrase = 'Un repas est constitué de '
    for s in range(len(u)-1):
        if s > 0:
            Phrase += ','
        gr = Qt[s]*100
        old_name = Al.iloc[u].index[s]
        name = rename_aliment(old_name)
        Phrase += ' de {:0.2f} g de {}'.format(gr, name)
    s = len(u)-1
    gr = Qt[s]*100
    old_name = Al.iloc[u].index[s]
    name = rename_aliment(old_name)
    Phrase += ' et de {:0.2f} g de {}. '.format(gr, name)
    REPAS = apports(RESULT)
    Phrase += ' Il coûte un total de {:0.2f} euros et comprend {:0.2f} calories.'.format(
        RESULT.fun, REPAS['Energie (kcal)'][-1])
    return Phrase
