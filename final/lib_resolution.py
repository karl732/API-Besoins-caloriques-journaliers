"""Description.

Librairie de résolution du problème complet.
"""

import warnings
import numpy as np
import pandas as pd
import scipy.optimize as so
from serde.json import from_json, to_json

from .data import Donnees

# Extraire les valeurs associées à chaque aliment
Al = pd.read_csv('final\Aliments.csv', sep=';', index_col=0)
aliments = np.array(Al).T


def apports(RESULT) -> pd.DataFrame:
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


def rename_aliment(old_name) -> str:
    """
    Fonction qui permet d'enlever le type de chaque aliment de sorte à fournir un résultat plus clair.
    """
    new_name = old_name.replace("Lait – ", "")
    new_name = new_name.replace("Viande – ", "")
    new_name = new_name.replace("Poisson – ", "")
    new_name = new_name.replace("Légume – ", "")
    new_name = new_name.replace("Base – ", "")
    return new_name


def resoud(donnees: Donnees) -> str:
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
    coeff = aliments[:-1] 
    bdns = [(0,None) for k in range(41)]
    bdns[38] = (0,5)

    # Formater les contraintes des coûts
    # b_eq = contraintes_couts[0]

    # Formater les besoins journaliers
    # k = int
    with open('../donnees.json', 'r') as f:
        donnees = from_json(Donnees,f.read())
    betaFE = np.array(donnees.betaF)

    # Formater la fonction objectif(minimiser le coût)
    c = aliments[-1]

    # Résoudre le problème d'optimisation linéaire
    
    ## désactiver les avertissements de type "DeprecationWarning"
    warnings.simplefilter('ignore', DeprecationWarning)
    RESULT = so.linprog(c, A_ub=-coeff, b_ub=-betaFE, method='simplex', bounds=bdns)
    if RESULT.success !=True:
        raise ValueError("L'optimisation sans contraintes supplémentaires est un échec")
    RESULTF= so.linprog(c, A_ub=np.concatenate((-coeff,coeff),axis=0), b_ub=np.concatenate((-betaFE,1.1*betaFE),axis=0),method='simplex')
    if RESULTF.success !=True:
        raise ValueError("L'optimisation avec contraintes supplémentaires est un échec")
    
    ## réactiver les avertissements de type "DeprecationWarning"
    warnings.simplefilter('default', DeprecationWarning)
    
    # Formatter la solution sans limite
    A = RESULT.x
    u, = A.nonzero()
    Qt = A[u]
    Phrase = "Un repas sans contrainte supplémentaires est constitué de "
    for s in range(len(u)-1):
        if s > 0:
            Phrase += ","
        gr = Qt[s]*100
        old_name = Al.iloc[u].index[s]
        name = rename_aliment(old_name)
        Phrase += " de {:0.2f} g de {}".format(gr, name)
    s = len(u)-1
    gr = Qt[s]*100
    old_name = Al.iloc[u].index[s]
    name = rename_aliment(old_name)
    Phrase += " et de {:0.2f} g de {}. ".format(gr, name)
    REPAS = apports(RESULT)
    Phrase += " Il coûte un total de {:0.2f} euros et comprend {:0.2f} calories. Nous avons fixé une limite à la quantité de haricots blancs pour avoir un repas plus varié.".format(
        RESULT.fun, REPAS['Energie (kcal)'][-1])
    # Formatter la solution avec limite de 10%
    B = RESULTF.x
    u_2, = B.nonzero()
    Qt = A[u_2]
    Phrase_2 = " Un repas avec 10% de contraintes supplémentaires est constitué de "
    for s in range(len(u_2)-1):
        if s > 0:
            Phrase_2 += ","
        gr = Qt[s]*100
        old_name = Al.iloc[u_2].index[s]
        name = rename_aliment(old_name)
        Phrase_2 += " de {:0.2f} g de {}".format(gr, name)
    s = len(u_2)-1
    gr = Qt[s]*100
    old_name = Al.iloc[u_2].index[s]
    name = rename_aliment(old_name)
    Phrase_2 += " et de {:0.2f} g de {}. ".format(gr, name)
    REPAS = apports(RESULTF)
    Phrase_2 += " Il coûte un total de {:0.2f} euros et comprend {:0.2f} calories.".format(
        RESULTF.fun, REPAS['Energie (kcal)'][-1])
    return Phrase, Phrase_2