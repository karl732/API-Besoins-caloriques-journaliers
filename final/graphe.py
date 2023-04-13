import networkx as nx

def ajouter_noeuds(G, data):
    """
    Ajoute les noeuds au graphe G à partir des données.
    """
    for i, d in enumerate(data.aliments):
        G.add_node(i, nom=d.nom, categorie=d.categorie, calories=d.calories, prix=d.prix)

def ajouter_arcs(G, data):
    """
    Ajoute les arcs au graphe G à partir des données.
    """
    for i, d in enumerate(data.aliments):
        for j, d2 in enumerate(data.aliments):
            if i != j and d.categorie == d2.categorie:
                G.add_edge(i, j, poids=d.distance(d2))

def graphe(data):
    """
    Construit un graphe à partir des données.
    """
    G = nx.Graph()
    ajouter_noeuds(G, data)
    ajouter_arcs(G, data)
    return G