import networkx as nx
from dataclasses import dataclass

def ajouter_noeuds(G, data):
    """
    Ajoute les noeuds au graphe G à partir des données.
    """
    for i, d in enumerate(data.aliments):
        G.add_node(i, nom=d.nom, categorie=d.categorie, calories=d.calories, prix=d.prix)

def ajouter_arretes(G, data):
    """
    Ajoute les arretes au graphe G à partir des données.
    """
    for i, d in enumerate(data.aliments):
        for j, d2 in enumerate(data.aliments):
            if i != j and d.categorie == d2.categorie:
                G.add_edge(i, j, poids=d.distance(d2))

def construit_graphe(data):
    """
    Construit un graphe à partir des données.
    """
    G = nx.Graph()
    ajouter_noeuds(G, data)
    ajouter_arretes(G, data)
    return G