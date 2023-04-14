"""Description.

Fonctionnalités de conversion du problème brute vers un graphe.
"""

from .data import Donnees
from enum import Enum
from itertools import product

import networkx as nx

def problem_to_graph(dp):
    # Création du graphe
    G = nx.DiGraph()

    # Ajout des nœuds ingrédients
    for i, ingredient_name in enumerate(dp.get_ingredient_names()):
        G.add_node(ingredient_name, bipartite=0, nutrient_contribution=dp.coeff_df.iloc[:, i].tolist())
        
    # Ajout des nœuds nutriments
    for j, nutrient_name in enumerate(dp.get_nutrient_names()):
        G.add_node(nutrient_name, bipartite=1, nutrient_requirement=dp.Marie_df.loc[nutrient_name, "Marie"])
    
    # Ajout des arrêtes entre ingrédients et nutriments
    for i in range(dp.coeff.shape[1]):
        for j in range(dp.coeff.shape[0] - 1):
            if dp.coeff[j, i] != 0:
                G.add_edge(dp.get_ingredient_names()[i], dp.get_nutrient_names()[j], weight=dp.coeff[j, i])

    return G
