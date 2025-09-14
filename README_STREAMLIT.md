# 🍽️ Application Streamlit - Optimiseur de Repas Journaliers

## 📖 Description

Cette application web interactive permet d'optimiser vos repas journaliers en fonction de vos besoins nutritionnels personnels et de vos contraintes budgétaires.

## 🚀 Lancement rapide

### Option 1: Script automatique
```bash
python lancer_app.py
```

### Option 2: Commande directe
```bash
streamlit run app_streamlit.py
```

### Option 3: Via le module
```bash
python -m streamlit run app_streamlit.py
```

## 🌐 Accès à l'application

Une fois lancée, l'application sera accessible à l'adresse :
- **URL locale** : http://localhost:8501
- **URL réseau** : http://[votre-ip]:8501 (si accessible depuis d'autres machines)

## 📱 Fonctionnalités

### 🏠 Page d'accueil
- **Explication complète** du fonctionnement de l'optimisation
- **Exemple visuel** avec graphiques
- **Guide d'utilisation** étape par étape

### 📊 Calculateur
- **Saisie personnalisée** des besoins nutritionnels :
  - Énergie (kcal)
  - Protéines (g)
  - Glucides (g)
  - Lipides (g)
  - Fer (mg)
  - Calcium (mg)
  - Fibres (g)

- **Contraintes personnalisables** :
  - Budget maximum (€)
  - Marge de sécurité nutritionnelle (%)
  - Limitation des haricots blancs (pour plus de variété)

- **Résultats détaillés** :
  - Menu optimal de base
  - Menu avec marge de sécurité
  - Coût total de chaque menu
  - Apports nutritionnels détaillés

### ℹ️ À propos
- **Détails techniques** sur les algorithmes utilisés
- **Base de données** des 41 aliments
- **Informations** sur les technologies employées

## 🎯 Valeurs recommandées

### Adulte moyen (2000 kcal)
- **Énergie** : 1800-2500 kcal
- **Protéines** : 50-100g
- **Glucides** : 150-300g
- **Lipides** : 50-120g
- **Fer** : 8-15mg
- **Calcium** : 800-1000mg
- **Fibres** : 25-35g

### Budget suggéré
- **Économique** : 2-5€
- **Standard** : 5-10€
- **Confort** : 10-20€

### Marge de sécurité
- **Minimale** : 5-10%
- **Recommandée** : 10-20%
- **Élevée** : 20-30%

## 🔧 Dépendances

L'application nécessite les packages suivants :
- `streamlit` >= 1.28.0
- `pandas` >= 2.0.1
- `numpy` >= 1.24.0
- `scipy` >= 1.10.0
- `rich` >= 11.2.0

## 🐛 Dépannage

### Problème : Streamlit non reconnu
```bash
pip install streamlit
```

### Problème : Modules non trouvés
Assurez-vous d'être dans le bon répertoire :
```bash
cd "Calcul de besoins journaliers API"
python lancer_app.py
```

### Problème : Port 8501 occupé
```bash
streamlit run app_streamlit.py --server.port 8502
```

### Problème : Optimisation échoue
- Augmentez le budget maximum
- Réduisez la marge de sécurité
- Désactivez la limitation des haricots blancs
- Vérifiez que vos besoins nutritionnels sont réalistes

## 📊 Exemple d'utilisation

1. **Lancez l'application** : `python lancer_app.py`
2. **Ouvrez votre navigateur** : http://localhost:8501
3. **Allez sur "Calculateur"** dans la sidebar
4. **Saisissez vos besoins** : par exemple 2000 kcal, 75g protéines...
5. **Définissez vos contraintes** : budget 10€, marge 15%
6. **Cliquez sur "Calculer"** et obtenez votre menu optimal !

## 🎨 Captures d'écran

L'application propose une interface moderne et intuitive avec :
- **Navigation par sidebar** pour accéder aux différentes pages
- **Formulaires interactifs** avec validation en temps réel
- **Graphiques dynamiques** pour visualiser les résultats
- **Messages d'aide** contextuels pour guider l'utilisateur
- **Design responsive** qui s'adapte à tous les écrans

## 🤝 Support

Si vous rencontrez des problèmes :
1. Vérifiez que tous les fichiers sont présents
2. Assurez-vous que les dépendances sont installées
3. Consultez les messages d'erreur dans le terminal
4. Essayez les différentes options de lancement

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
