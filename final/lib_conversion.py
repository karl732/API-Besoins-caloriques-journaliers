"""Description.
    
    Pour transformer le problème d'optimisation en graphe dirigé, il est possible d'utiliser le
    concept de graphe de flux, aussi appelé graphe de circulation. Ce type de graphe est
    utilisé pour représenter un réseau de flux, où chaque nœud est un point de
    distribution ou de collecte, et chaque arête représente un canal de transport de 
    ressources entre deux nœuds.

Dans le cas de notre problème d'optimisation de menu alimentaire, nous pouvons modéliser
le graphe de flux comme suit:

- Les nœuds sources représentent les aliments disponibles et les nœuds puits représentent
les besoins nutritionnels journaliers.
- Les arêtes représentent les quantités d'un nutriment spécifique fourni par un aliment
donné.
- Les poids des arêtes peuvent représenter le coût ou la quantité d'un nutriment fourni
par une unité d'aliment.
"""

import networkx as nx

# Definir le problème
nutriments = ["Kcal", "Protéines", "Glucides", "Lipides", "Fer", "Calcium", "Fibre"]
aliments = ["A1", "A2", "A3", "A4", "A5"]
apports_nutritionnels = [    [50, 3, 20, 10, 1, 100, 5],
    [200, 8, 15, 20, 2, 50, 2],
    [150, 6, 10, 15, 1, 80, 2],
    [100, 4, 5, 8, 0.5, 30, 1],
    [80, 2, 3, 6, 0.3, 20, 1]
]
prix = [0.4, 0.5, 0.6, 0.3, 0.2]
contraintes_nutriments = [    ("Kcal", 2000),    ("Protéines", 75),    ("Glucides", 225),    ("Lipides", 90),    ("Fer", 9),    ("Calcium", 800),    ("Fibre", 45)]

# Create the graph
G = nx.DiGraph()

# ajouter les noeuds
for aliment in aliments:
    G.add_node(aliment)

G.add_node("source")
G.add_node("sink")

# ajouter les arretes
for i, aliment in enumerate(aliments):
    G.add_edge("source", aliment, capacity=1, weight=0)
    G.add_edge(aliment, "sink", capacity=1, weight=prix[i])
    for j, nutriment in enumerate(nutriments):
        G.add_edge(aliment, nutriment, capacity=apports_nutritionnels[i][j], weight=0)
        G.add_edge(nutriment, "sink", capacity=contraintes_nutriments[j][1], weight=0)

# trouver les flows maximum et minimum
flowCost, flowDict = nx.network_simplex(G, weight="weight")
print("Maximum flow:", flowCost)
print("Minimum cost:", flowDict["sink"]["flow"] * flowCost)