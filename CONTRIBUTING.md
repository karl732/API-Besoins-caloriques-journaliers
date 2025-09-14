# 🤝 Guide de Contribution

Merci de votre intérêt pour contribuer à l'Optimiseur de Repas Journaliers ! Ce guide vous aidera à comprendre comment participer au projet.

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.9 ou supérieur
- Git
- Un éditeur de code (VSCode recommandé)

### Installation pour le Développement

```bash
# 1. Fork le projet sur GitHub
# 2. Cloner votre fork
git clone https://github.com/VOTRE-USERNAME/optimiseur-repas-journaliers.git
cd optimiseur-repas-journaliers

# 3. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Installer les dépendances de développement
pip install pytest black mypy pylama

# 6. Tester l'installation
python test_streamlit_app.py
streamlit run app_streamlit.py
```

## 📋 Types de Contributions

### 🐛 Signaler des Bugs
- Utilisez les [GitHub Issues](https://github.com/karlsondeji/optimiseur-repas-journaliers/issues)
- Décrivez clairement le problème
- Incluez les étapes de reproduction
- Précisez votre environnement (OS, Python version, etc.)

### ✨ Proposer des Fonctionnalités
- Créez une issue avec le label "enhancement"
- Décrivez le cas d'usage
- Expliquez pourquoi cette fonctionnalité serait utile
- Proposez une implémentation si possible

### 🔧 Corriger des Bugs
1. Assignez-vous l'issue correspondante
2. Créez une branche : `git checkout -b fix/nom-du-bug`
3. Implémentez la correction
4. Ajoutez des tests si nécessaire
5. Soumettez une Pull Request

### 📚 Améliorer la Documentation
- Corrigez les typos
- Clarifiez les explications
- Ajoutez des exemples
- Traduisez en d'autres langues

## 🔄 Processus de Développement

### Workflow Git
```bash
# 1. Créer une branche pour votre feature
git checkout -b feature/nom-de-la-feature

# 2. Faire vos modifications
# ... développement ...

# 3. Tester vos modifications
python -m pytest tests/
python test_streamlit_app.py
black *.py
mypy *.py

# 4. Commiter vos changements
git add .
git commit -m "feat: description claire de la fonctionnalité"

# 5. Pousser vers votre fork
git push origin feature/nom-de-la-feature

# 6. Créer une Pull Request sur GitHub
```

### Standards de Code

#### Style Python
- Suivre PEP 8
- Utiliser Black pour le formatage : `black *.py`
- Longueur de ligne : 88 caractères
- Utiliser des noms de variables descriptifs

#### Documentation
```python
def ma_fonction(param1: int, param2: str) -> bool:
    """Description courte de la fonction.
    
    Description plus détaillée si nécessaire.
    
    Args:
        param1: Description du paramètre 1
        param2: Description du paramètre 2
        
    Returns:
        Description de ce qui est retourné
        
    Raises:
        ValueError: Quand param1 est négatif
    """
    pass
```

#### Tests
```python
def test_ma_fonction():
    """Test de ma_fonction avec des cas normaux."""
    # Arrange
    input_value = 42
    expected = True
    
    # Act
    result = ma_fonction(input_value, "test")
    
    # Assert
    assert result == expected
```

### Conventions de Commit

Utilisez le format [Conventional Commits](https://www.conventionalcommits.org/) :

- `feat:` nouvelle fonctionnalité
- `fix:` correction de bug
- `docs:` documentation
- `style:` formatage, points-virgules manquants, etc.
- `refactor:` refactoring du code
- `test:` ajout de tests
- `chore:` maintenance

Exemples :
```bash
git commit -m "feat: ajouter contrainte budgétaire dans l'interface"
git commit -m "fix: corriger calcul des calories pour les légumes"
git commit -m "docs: améliorer README avec exemples d'utilisation"
```

## 🧪 Tests

### Lancer les Tests
```bash
# Tests unitaires
python -m pytest tests/

# Tests d'intégration
python test_streamlit_app.py

# Tests de style
black --check *.py
mypy *.py
pylama *.py
```

### Ajouter des Tests
- Créez des fichiers `test_*.py` dans le dossier `tests/`
- Testez les cas normaux et les cas d'erreur
- Visez une couverture de code élevée
- Utilisez des fixtures pour les données de test

## 📊 Structure du Projet

```
optimiseur-repas-journaliers/
├── 📁 final/                 # Module principal
│   ├── __init__.py
│   ├── data.py              # Classes de données
│   ├── lib_resolution.py    # Algorithmes d'optimisation
│   └── Aliments.csv         # Base de données nutritionnelle
├── 📁 tests/                # Tests unitaires
├── app_streamlit.py         # Interface web Streamlit
├── __main__.py              # CLI principale
├── lancer_app.py           # Script de lancement
├── test_streamlit_app.py   # Tests d'intégration
├── pyproject.toml          # Configuration Poetry
├── requirements.txt        # Dépendances pip
└── README.md              # Documentation principale
```

## 🎯 Domaines de Contribution

### 🔢 Algorithmes
- Améliorer les performances d'optimisation
- Ajouter de nouveaux solveurs
- Implémenter des heuristiques
- Optimiser la gestion mémoire

### 🎨 Interface Utilisateur
- Améliorer l'UX Streamlit
- Ajouter des visualisations
- Créer des thèmes
- Optimiser la responsivité

### 📊 Données
- Étendre la base alimentaire
- Ajouter des profils nutritionnels
- Intégrer des APIs externes
- Valider les données existantes

### 🌍 Internationalisation
- Traduire l'interface
- Adapter les unités de mesure
- Localiser les données nutritionnelles
- Créer des guides régionaux

### 🔧 Infrastructure
- Améliorer les tests
- Optimiser les performances
- Ajouter des métriques
- Créer des pipelines CI/CD

## ❓ Questions et Support

### Où Demander de l'Aide ?
1. **Documentation** : Consultez d'abord le README et les docstrings
2. **Issues** : Recherchez dans les issues existantes
3. **Discussions** : Utilisez les GitHub Discussions pour les questions générales
4. **Email** : Contactez directement pour les questions sensibles

### Ressources Utiles
- [Documentation SciPy](https://docs.scipy.org/doc/scipy/reference/optimize.html)
- [Guide Streamlit](https://docs.streamlit.io/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## 🏆 Reconnaissance

Tous les contributeurs seront ajoutés au fichier CONTRIBUTORS.md et mentionnés dans les releases notes.

### Niveaux de Contribution
- 🌟 **Contributeur** : 1+ PR mergée
- 🚀 **Contributeur Actif** : 5+ PRs mergées
- 🏆 **Mainteneur** : Contributions régulières + responsabilités de maintenance

## 📄 Licence

En contribuant, vous acceptez que vos contributions soient sous licence MIT, comme le reste du projet.

---

**Merci de contribuer à rendre l'optimisation nutritionnelle accessible à tous ! 🍽️❤️**
