"""Description.

Librairie de résolution du problème complet.
"""

import warnings
import numpy as np
import pandas as pd
import scipy.optimize as so
from serde.json import from_json, to_json

from .data import Donnees
from typing import Tuple
from rich import print


# Extraire les valeurs associées à chaque aliment
import os
csv_path = os.path.join(os.path.dirname(__file__), 'Aliments.csv')
Al = pd.read_csv(csv_path, sep=';', index_col=0)
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
    total_row = pd.DataFrame([REPAS.sum()], index=['Apports du repas'])
    REPAS = pd.concat([REPAS, total_row])
    Namescol = ['Quantité (en g)']+list(Al.columns)
    Namescol[-1] = 'Prix (en €)'
    REPAS.columns = Namescol
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


def valider_donnees(donnees: Donnees) -> None:
    """Valide et affiche des avertissements pour les données d'entrée."""
    nutriments = ["Kcal", "Protéines", "Glucides", "Lipides", "Fer", "Calcium", "Fibres"]
    valeurs_min = [50, 1, 5, 1, 0.1, 10, 1]  
    valeurs_max = [10000, 500, 2000, 500, 100, 5000, 500]
    
    for i, valeur in enumerate(donnees.betaF):
        if valeur < valeurs_min[i]:
            print(f"[yellow]⚠️  Attention: La valeur pour {nutriments[i]} ({valeur}) est très faible. "
                  f"Minimum recommandé: {valeurs_min[i]}[/yellow]")
        
        if valeur > valeurs_max[i]:
            print(f"[yellow]⚠️  Attention: La valeur pour {nutriments[i]} ({valeur}) est très élevée. "
                  f"Maximum recommandé: {valeurs_max[i]}[/yellow]")


def resoud(donnees: Donnees) -> Tuple[str, str]:
    """Résout le problème d'optimisation alimentaire.

    Trouve la combinaison d'aliments optimale pour satisfaire les besoins nutritionnels
    au coût minimum, avec et sans contraintes supplémentaires.
    
    Args:
        donnees: Objet contenant les besoins nutritionnels journaliers.

    Returns:
        tuple: (solution_sans_contraintes, solution_avec_contraintes)
            Phrases décrivant les solutions d'optimisation.
    """
    # Valider les données et afficher des avertissements si nécessaire
    valider_donnees(donnees)
    # Extraire les données de l'objet Donnees
    # nutriments = Donnees.nutriments
    # aliments_index = Donnees.aliments_index
    # contraintes_aliments = Donnees.contraintes_aliments
    # contraintes_couts = Donnees.contraintes_couts
    # besoins_journaliers = Donnees.besoins_journaliers

    # Formater les contraintes des aliments
    # Réorganiser les colonnes pour correspondre à l'ordre de betaF
    # CSV: Protéines, Lipides, Glucides, Energie (kcal), Fer, Calcium, Fibres, Prix
    # betaF: [Kcal, Protéines, Glucides, Lipides, Fer, Calcium, Fibres]
    # Réorganisation : [3, 0, 2, 1, 4, 5, 6] (indices du CSV)
    coeff_reordered = np.array([
        aliments[3],  # Energie (kcal)
        aliments[0],  # Protéines  
        aliments[2],  # Glucides
        aliments[1],  # Lipides
        aliments[4],  # Fer
        aliments[5],  # Calcium
        aliments[6]   # Fibres
    ])
    
    bdns = [(0, None) for k in range(41)]
    bdns[38] = (0, 5)  # Limite sur les haricots blancs

    # Formater les besoins journaliers
    betaFE = np.array(donnees.betaF)

    # Formater la fonction objectif(minimiser le coût)
    c = aliments[-1]

    # Résoudre le problème d'optimisation linéaire
    
    ## désactiver les avertissements de type "DeprecationWarning"
    warnings.simplefilter('ignore', DeprecationWarning)
    
    # Première optimisation : solution de base (contraintes minimales)
    RESULT = None
    methods = ['highs', 'simplex', 'interior-point']
    
    for method in methods:
        try:
            RESULT = so.linprog(c, A_ub=-coeff_reordered, b_ub=-betaFE, method=method, bounds=bdns)
            if RESULT.success:
                break
        except:
            continue
    
    if RESULT is None or not RESULT.success:
        # Essayer sans la contrainte sur les haricots blancs
        bdns_relaxed = [(0, None) for k in range(41)]
        for method in methods:
            try:
                RESULT = so.linprog(c, A_ub=-coeff_reordered, b_ub=-betaFE, method=method, bounds=bdns_relaxed)
                if RESULT.success:
                    break
            except:
                continue
    
    if RESULT is None or not RESULT.success:
        raise ValueError("Impossible de trouver une solution même avec des contraintes relaxées")
    
    # Deuxième optimisation : solution avec contraintes supplémentaires
    RESULTF = None
    constraint_factors = [1.1, 1.2, 1.5, 2.0]  # Essayer différents niveaux de tolérance
    used_factor = None
    
    for factor in constraint_factors:
        for method in methods:
            try:
                RESULTF = so.linprog(c, 
                                   A_ub=np.concatenate((-coeff_reordered, coeff_reordered), axis=0), 
                                   b_ub=np.concatenate((-betaFE, factor*betaFE), axis=0), 
                                   method=method, bounds=bdns)
                if RESULTF.success:
                    used_factor = factor
                    break
            except:
                continue
        if RESULTF is not None and RESULTF.success:
            break
    
    # Si aucune solution avec contraintes supplémentaires n'est trouvée, utiliser la solution de base
    if RESULTF is None or not RESULTF.success:
        RESULTF = RESULT
        constraint_used = "aucune contrainte supplémentaire (solution identique à la première)"
    else:
        constraint_used = f"{int((used_factor-1)*100)}% de contraintes supplémentaires"
    
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
        RESULT.fun, REPAS['Energie (kcal)'].iloc[-1])
    # Formatter la solution avec contraintes supplémentaires
    B = RESULTF.x
    u_2, = B.nonzero()
    Qt_2 = B[u_2]
    Phrase_2 = f" Un repas avec {constraint_used} est constitué de "
    for s in range(len(u_2)-1):
        if s > 0:
            Phrase_2 += ","
        gr = Qt_2[s]*100
        old_name = Al.iloc[u_2].index[s]
        name = rename_aliment(old_name)
        Phrase_2 += " de {:0.2f} g de {}".format(gr, name)
    s = len(u_2)-1
    gr = Qt_2[s]*100
    old_name = Al.iloc[u_2].index[s]
    name = rename_aliment(old_name)
    Phrase_2 += " et de {:0.2f} g de {}. ".format(gr, name)
    REPAS = apports(RESULTF)
    Phrase_2 += " Il coûte un total de {:0.2f} euros et comprend {:0.2f} calories.".format(
        RESULTF.fun, REPAS['Energie (kcal)'].iloc[-1])
    return Phrase, Phrase_2


def resoud_avec_contraintes(donnees: Donnees, budget_max: float = None, 
                           marge_pourcentage: float = 0.1, 
                           limite_haricots: bool = True) -> Tuple[str, str]:
    """Résout le problème d'optimisation avec contraintes personnalisées.
    
    Args:
        donnees: Besoins nutritionnels
        budget_max: Budget maximum en euros (None = pas de limite)
        marge_pourcentage: Pourcentage de marge (0.1 = 10%)
        limite_haricots: Limiter les haricots blancs à 500g
        
    Returns:
        tuple: (solution_base, solution_avec_marge)
    """
    # Valider les données et afficher des avertissements si nécessaire
    valider_donnees(donnees)
    
    # Formater les contraintes des aliments
    coeff_reordered = np.array([
        aliments[3],  # Energie (kcal)
        aliments[0],  # Protéines  
        aliments[2],  # Glucides
        aliments[1],  # Lipides
        aliments[4],  # Fer
        aliments[5],  # Calcium
        aliments[6]   # Fibres
    ])
    
    # Contraintes sur les quantités d'aliments
    bdns = [(0, None) for k in range(41)]
    if limite_haricots:
        bdns[38] = (0, 5)  # Limite sur les haricots blancs
    
    betaFE = np.array(donnees.betaF)
    c = aliments[-1]  # Coûts
    
    # Si budget maximum spécifié, ajouter la contrainte budgétaire
    if budget_max is not None:
        # Ajouter la contrainte : somme(prix_i * quantité_i) <= budget_max
        coeff_budget = np.vstack([coeff_reordered, c.reshape(1, -1)])
        besoins_budget = np.append(betaFE, budget_max)
    else:
        coeff_budget = coeff_reordered
        besoins_budget = betaFE
    
    ## Optimisation
    warnings.simplefilter('ignore', DeprecationWarning)
    
    # Première optimisation : solution de base
    RESULT = None
    methods = ['highs', 'simplex', 'interior-point']
    
    for method in methods:
        try:
            RESULT = so.linprog(c, A_ub=-coeff_budget, b_ub=-besoins_budget, 
                              method=method, bounds=bdns)
            if RESULT.success:
                break
        except:
            continue
    
    # Relaxation si nécessaire
    if RESULT is None or not RESULT.success:
        if budget_max is not None:
            # Essayer sans contrainte budgétaire
            for method in methods:
                try:
                    RESULT = so.linprog(c, A_ub=-coeff_reordered, b_ub=-betaFE, 
                                      method=method, bounds=bdns)
                    if RESULT.success:
                        break
                except:
                    continue
        
        if RESULT is None or not RESULT.success:
            # Essayer sans limite haricots
            bdns_relaxed = [(0, None) for k in range(41)]
            for method in methods:
                try:
                    RESULT = so.linprog(c, A_ub=-coeff_reordered, b_ub=-betaFE, 
                                      method=method, bounds=bdns_relaxed)
                    if RESULT.success:
                        break
                except:
                    continue
    
    if RESULT is None or not RESULT.success:
        raise ValueError("Impossible de trouver une solution. Essayez d'augmenter le budget ou de réduire les contraintes.")
    
    # Deuxième optimisation avec marge
    RESULTF = None
    if marge_pourcentage > 0:
        marge_factor = 1 + marge_pourcentage
        
        # Contraintes avec marge
        if budget_max is not None:
            coeff_marge = np.vstack([
                np.concatenate((-coeff_reordered, coeff_reordered), axis=0),
                np.concatenate((-c.reshape(1, -1), c.reshape(1, -1)), axis=0)
            ])
            besoins_marge = np.concatenate([
                -betaFE, marge_factor * betaFE, [-budget_max, budget_max]
            ])
        else:
            coeff_marge = np.concatenate((-coeff_reordered, coeff_reordered), axis=0)
            besoins_marge = np.concatenate((-betaFE, marge_factor * betaFE))
        
        for method in methods:
            try:
                RESULTF = so.linprog(c, A_ub=coeff_marge, b_ub=besoins_marge, 
                                   method=method, bounds=bdns)
                if RESULTF.success:
                    break
            except:
                continue
    
    # Si pas de solution avec marge, utiliser la solution de base
    if RESULTF is None or not RESULTF.success:
        RESULTF = RESULT
        constraint_used = "aucune marge supplémentaire (solution identique)"
    else:
        constraint_used = f"{int(marge_pourcentage*100)}% de marge nutritionnelle"
    
    warnings.simplefilter('default', DeprecationWarning)
    
    # Formatter les solutions
    phrase_base = formatter_solution(RESULT, "sans contrainte supplémentaire")
    phrase_marge = formatter_solution(RESULTF, f"avec {constraint_used}")
    
    return phrase_base, phrase_marge


def formatter_solution(result, description: str) -> str:
    """Formate la solution d'optimisation en phrase lisible."""
    A = result.x
    u, = A.nonzero()
    Qt = A[u]
    
    if len(u) == 0:
        return f"Aucune solution trouvée pour {description}."
    
    phrase = f"Un repas {description} est constitué de "
    
    for s in range(len(u)-1):
        if s > 0:
            phrase += ", "
        gr = Qt[s] * 100
        old_name = Al.iloc[u[s]].name
        name = rename_aliment(old_name)
        phrase += f"{gr:.1f}g de {name}"
    
    # Dernier élément
    if len(u) > 1:
        s = len(u) - 1
        gr = Qt[s] * 100
        old_name = Al.iloc[u[s]].name
        name = rename_aliment(old_name)
        phrase += f" et {gr:.1f}g de {name}"
    
    # Calcul des totaux
    repas = apports(result)
    cout = result.fun
    calories = repas['Energie (kcal)'].iloc[-1]
    
    phrase += f". Il coûte {cout:.2f}€ et apporte {calories:.0f} calories."
    
    return phrase