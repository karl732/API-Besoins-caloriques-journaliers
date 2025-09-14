"""Point d'entrée pour le module final."""

import sys
import os

# Ajouter le répertoire parent au path pour pouvoir importer le module racine
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_dir)

# Importer et exécuter l'application principale depuis le fichier main du projet
main_file = os.path.join(parent_dir, '__main__.py')
with open(main_file) as f:
    code = compile(f.read(), main_file, 'exec')
    exec(code)
