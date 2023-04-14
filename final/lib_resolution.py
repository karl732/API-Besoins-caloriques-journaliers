import __main__ as dp
from conversion import *
import numpy as np
from scipy.optimize import linprog
from conversion import convert_data


def solve_diet_problem():
    # Conversion des données en numpy arrays
    A, b, c = convert_data(dp)
    # Résolution du problème
    res = linprog(c, A_eq=A, b_eq=b, bounds=(0, None), method='simplex')
    # Affichage des résultats
    x = res.x
    print("Le coût minimum est de :", round(res.fun, 2), "€.")
    print("Les quantités à prendre pour avoir un régime équilibré sont les suivantes :")
    for i in range(len(x)):
        print(dp['Aliment'][i], round(x[i], 2), dp['Unité'][i])
        print("total coûts des ingrédients = ", round(np.dot(c, x), 2))