import networkx as nx
from final.data import Donnees

# Données du problème
aliments = {
    'pomme': {'calories': 95, 'proteines': 0.3, 'glucides': 25, 'lipides': 0.4, 'fer': 0.2},
    'banane': {'calories': 105, 'proteines': 1.3, 'glucides': 27, 'lipides': 0.4, 'fer': 0.3},
    'yaourt': {'calories': 150, 'proteines': 5, 'glucides': 17, 'lipides': 8, 'fer': 0.1},
    'salade': {'calories': 5, 'proteines': 0.5, 'glucides': 1, 'lipides': 0.1, 'fer': 0.2},
    'poulet': {'calories': 165, 'proteines': 31, 'glucides': 0, 'lipides': 3.6, 'fer': 0.2},
    'oeuf': {'calories': 78, 'proteines': 6, 'glucides': 0.6, 'lipides': 5.3, 'fer': 0.3},
}

besoins_journaliers = {
    'Kcal': 2000,
    'Protéines': 75,
    'Glucides': 225,
    'Lipides': 90,
    'Fer': 9,
    'Fibre': 45,
}

# Construction du graphe
G = nx.DiGraph()
for aliment, nutriments in aliments.items():
    G.add_node(aliment, nutriments=nutriments)
    for nutriment, besoin in besoins_journaliers.items():
        G.add_node(nutriment, besoin=besoin)
        for aliment, nutriments in aliments.items():
            if nutriment in nutriments:
                G.add_edge(nutriment, aliment, weight=nutriments[nutriment])

# Fonction de recherche de chemin le plus court
def find_shortest_path(G, source, target):
    try:
        path = nx.shortest_path(G, source=source, target=target, weight='weight')
        return path
    except:
        return None


# Résolution du problème
menu = []
for nutriment, besoin in besoins_journaliers.items():
    for aliment, nutriments in aliments.items():
        if nutriment in nutriments:
            path = find_shortest_path(G, nutriment, aliment)