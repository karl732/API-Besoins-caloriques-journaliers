"""
Application Streamlit pour l'optimisation des repas journaliers.

Cette application permet aux utilisateurs de définir leurs besoins nutritionnels
personnels et leurs contraintes budgétaires pour obtenir un menu optimisé.
"""

import streamlit as st
import pandas as pd
import numpy as np
from final.data import Donnees
from final.lib_resolution import resoud_avec_contraintes
import json

def main():
    """Fonction principale de l'application Streamlit."""
    
    # Configuration de la page
    st.set_page_config(
        page_title="Optimiseur de Repas Journaliers",
        page_icon="🍽️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Titre principal
    st.title("🍽️ Optimiseur de Repas Journaliers")
    st.markdown("---")
    
    # Sidebar pour la navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choisissez une page:",
        ["🏠 Accueil", "📊 Calculateur", "ℹ️ À propos"]
    )
    
    if page == "🏠 Accueil":
        page_accueil()
    elif page == "📊 Calculateur":
        page_calculateur()
    elif page == "ℹ️ À propos":
        page_apropos()

def page_accueil():
    """Page d'accueil avec explication du programme."""
    
    st.header("Bienvenue dans l'Optimiseur de Repas Journaliers")
    
    st.markdown("""
    ### 🎯 Objectif
    Cette application résout un **problème d'optimisation linéaire** pour vous proposer 
    le menu le plus économique qui satisfait vos besoins nutritionnels journaliers.
    
    ### 🔬 Comment ça fonctionne ?
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1. Données d'entrée**
        - 📋 Base de données de 41 aliments avec leurs valeurs nutritionnelles
        - 🎯 Vos besoins journaliers personnalisés
        - 💰 Vos contraintes budgétaires
        
        **2. Optimisation**
        - ⚙️ Algorithme de programmation linéaire
        - 🎯 Objectif : minimiser le coût
        - ✅ Contraintes : respecter vos besoins nutritionnels
        """)
    
    with col2:
        st.markdown("""
        **3. Résultats**
        - 🍽️ Menu optimal de base
        - 🍽️ Menu avec marge de sécurité (optionnel)
        - 💰 Coût total de chaque menu
        - 📊 Détail des apports nutritionnels
        
        **4. Avantages**
        - 💰 Économique
        - 🥗 Nutritionnellement équilibré
        - ⚡ Rapide et précis
        """)
    
    st.markdown("---")
    
    # Exemple visuel
    st.subheader("📈 Exemple de résolution")
    
    # Création d'un graphique exemple
    example_data = {
        'Nutriment': ['Kcal', 'Protéines', 'Glucides', 'Lipides', 'Fer', 'Calcium', 'Fibres'],
        'Besoin': [2000, 75, 225, 90, 9, 800, 45],
        'Apport Menu': [2000, 78, 230, 88, 9.5, 820, 47]
    }
    
    df_example = pd.DataFrame(example_data)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.bar_chart(df_example.set_index('Nutriment')[['Besoin', 'Apport Menu']])
    
    with col2:
        st.metric("Coût optimal", "2.49 €")
        st.metric("Écart moyen", "+3.2%")
        st.metric("Aliments utilisés", "5")
    
    st.markdown("---")
    
    st.info("👈 Utilisez le **Calculateur** dans la sidebar pour créer votre menu personnalisé !")

def page_calculateur():
    """Page principale du calculateur."""
    
    st.header("📊 Calculateur de Menu Optimal")
    
    # Section 1: Besoins nutritionnels
    st.subheader("1. 🥗 Vos besoins nutritionnels journaliers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        energie = st.number_input(
            "Énergie (kcal)", 
            min_value=800, 
            max_value=5000, 
            value=2000, 
            step=50,
            help="Besoins énergétiques quotidiens (adulte moyen: 1800-2500 kcal)"
        )
        
        proteines = st.number_input(
            "Protéines (g)", 
            min_value=20, 
            max_value=200, 
            value=75, 
            step=5,
            help="Besoins en protéines (adulte: 0.8-1.2g/kg de poids corporel)"
        )
        
        glucides = st.number_input(
            "Glucides (g)", 
            min_value=50, 
            max_value=500, 
            value=225, 
            step=10,
            help="Besoins en glucides (45-65% de l'apport énergétique total)"
        )
        
        lipides = st.number_input(
            "Lipides (g)", 
            min_value=20, 
            max_value=150, 
            value=90, 
            step=5,
            help="Besoins en lipides (20-35% de l'apport énergétique total)"
        )
    
    with col2:
        fer = st.number_input(
            "Fer (mg)", 
            min_value=5.0, 
            max_value=30.0, 
            value=9.0, 
            step=0.5,
            help="Besoins en fer (hommes: 8mg, femmes: 15mg)"
        )
        
        calcium = st.number_input(
            "Calcium (mg)", 
            min_value=400, 
            max_value=1500, 
            value=800, 
            step=50,
            help="Besoins en calcium (adultes: 800-1000mg)"
        )
        
        fibres = st.number_input(
            "Fibres (g)", 
            min_value=15, 
            max_value=80, 
            value=45, 
            step=5,
            help="Besoins en fibres (adultes: 25-35g)"
        )
    
    st.markdown("---")
    
    # Section 2: Contraintes
    st.subheader("2. 💰 Contraintes et préférences")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        budget_max = st.number_input(
            "Budget maximum (€)", 
            min_value=1.0, 
            max_value=50.0, 
            value=10.0, 
            step=0.5,
            help="Budget maximum que vous souhaitez consacrer à ce repas"
        )
    
    with col2:
        marge_securite = st.number_input(
            "Marge de sécurité (%)", 
            min_value=0, 
            max_value=100, 
            value=10, 
            step=5,
            help="Pourcentage supplémentaire au-dessus de vos besoins (recommandé: 10-20%)"
        )
    
    with col3:
        limite_haricots = st.checkbox(
            "Limiter les haricots blancs", 
            value=True,
            help="Limite la quantité de haricots blancs à 500g pour plus de variété"
        )
    
    st.markdown("---")
    
    # Section 3: Calcul
    st.subheader("3. 🔄 Calcul du menu optimal")
    
    if st.button("🚀 Calculer mon menu optimal", type="primary"):
        
        # Création de l'objet Donnees
        besoins = [energie, proteines, glucides, lipides, fer, calcium, fibres]
        donnees = Donnees(betaF=besoins)
        
        # Barre de progression
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("🔍 Analyse des données...")
            progress_bar.progress(25)
            
            status_text.text("⚙️ Optimisation en cours...")
            progress_bar.progress(50)
            
            # Appel de la fonction d'optimisation
            solution_base, solution_marge = resoud_avec_contraintes(
                donnees, 
                budget_max, 
                marge_securite/100, 
                limite_haricots
            )
            
            progress_bar.progress(75)
            status_text.text("📊 Génération des résultats...")
            
            progress_bar.progress(100)
            status_text.text("✅ Calcul terminé !")
            
            # Affichage des résultats
            st.success("🎉 Menu optimal calculé avec succès !")
            
            # Résultats en colonnes
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🍽️ **Menu de base**")
                st.markdown(solution_base)
            
            with col2:
                st.markdown(f"### 🍽️ **Menu avec {marge_securite}% de marge**")
                st.markdown(solution_marge)
            
        except Exception as e:
            st.error(f"❌ Erreur lors du calcul : {str(e)}")
            st.info("💡 Essayez de réduire vos contraintes ou d'augmenter votre budget.")
    
    # Section 4: Conseils
    with st.expander("💡 Conseils pour optimiser vos résultats"):
        st.markdown("""
        **Pour obtenir les meilleurs résultats :**
        
        - 🎯 **Besoins réalistes** : Utilisez des valeurs proches des recommandations nutritionnelles
        - 💰 **Budget suffisant** : Un budget trop faible peut rendre le problème impossible à résoudre
        - 📊 **Marge de sécurité** : 10-20% permet d'avoir une alimentation plus équilibrée
        - 🥗 **Variété** : Activez la limite sur les haricots blancs pour plus de diversité
        
        **Valeurs de référence pour un adulte moyen :**
        - Énergie : 1800-2500 kcal
        - Protéines : 50-100g
        - Glucides : 150-300g  
        - Lipides : 50-120g
        - Fer : 8-15mg
        - Calcium : 800-1000mg
        - Fibres : 25-35g
        """)

def page_apropos():
    """Page à propos avec informations techniques."""
    
    st.header("ℹ️ À propos de l'application")
    
    st.markdown("""
    ### 🔬 Méthode scientifique
    
    Cette application utilise la **programmation linéaire** pour résoudre un problème d'optimisation 
    sous contraintes. Plus précisément :
    
    - **Fonction objectif** : Minimiser le coût total du repas
    - **Variables de décision** : Quantité de chaque aliment (en portions de 100g)
    - **Contraintes** : Respecter les besoins nutritionnels minimaux
    - **Algorithmes** : Simplex, Points intérieurs, HiGHS
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 Base de données
        
        **41 aliments** répartis en catégories :
        - 🥛 Produits laitiers (9)
        - 🥩 Viandes et poissons (15)
        - 🥬 Légumes (9)
        - 🌾 Céréales et légumineuses (8)
        
        **8 critères nutritionnels** :
        - Protéines, Lipides, Glucides
        - Énergie (kcal)
        - Fer, Calcium, Fibres
        - Prix (€/100g)
        """)
    
    with col2:
        st.markdown("""
        ### ⚙️ Technologies utilisées
        
        - **Python** : Langage de programmation
        - **SciPy** : Optimisation linéaire
        - **Pandas** : Manipulation des données
        - **Streamlit** : Interface utilisateur
        - **Poetry** : Gestion des dépendances
        - **Pyserde** : Sérialisation JSON
        
        ### 🎯 Robustesse
        
        - **Multi-algorithmes** : 3 solveurs différents
        - **Contraintes adaptatives** : Relaxation automatique
        - **Validation des données** : Contrôles de cohérence
        """)
    
    st.markdown("---")
    
    # Informations sur les algorithmes
    with st.expander("🔧 Détails techniques des algorithmes"):
        st.markdown("""
        **1. Algorithme HiGHS** (par défaut)
        - Algorithme moderne et efficace
        - Bonne performance sur les problèmes de grande taille
        - Stable numériquement
        
        **2. Méthode du Simplexe**
        - Algorithme classique de programmation linéaire
        - Parcourt les sommets du domaine réalisable
        - Fallback si HiGHS échoue
        
        **3. Méthode des Points Intérieurs**
        - Traverse l'intérieur du domaine réalisable
        - Efficace pour les problèmes mal conditionnés
        - Dernier recours si les autres méthodes échouent
        
        **Stratégie de relaxation :**
        - Si aucune solution n'est trouvée, suppression progressive des contraintes
        - Augmentation automatique des marges de tolérance
        - Garantit de toujours trouver une solution réalisable
        """)
    
    # Contact et version
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**Version** : 1.0.0")
    
    with col2:
        st.info("**Auteur** : Karl Sondeji")
    
    with col3:
        st.info("**Licence** : MIT")

if __name__ == "__main__":
    main()
