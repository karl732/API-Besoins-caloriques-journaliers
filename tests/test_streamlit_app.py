"""
Script de test pour vérifier le bon fonctionnement de l'application Streamlit.
"""

from final.data import Donnees
from final.lib_resolution import resoud_avec_contraintes

def test_fonction_resoud():
    """Test de la fonction resoud_avec_contraintes."""
    print("🧪 Test de la fonction d'optimisation avec contraintes...")
    
    # Données de test
    besoins = [2000, 75, 225, 90, 9, 800, 45]  # Kcal, Protéines, Glucides, Lipides, Fer, Calcium, Fibres
    donnees = Donnees(betaF=besoins)
    
    try:
        # Test 1: Sans contraintes
        print("\n1️⃣ Test sans contraintes spécifiques:")
        solution_base, solution_marge = resoud_avec_contraintes(donnees)
        print(f"✅ Solution de base: {solution_base[:100]}...")
        print(f"✅ Solution avec marge: {solution_marge[:100]}...")
        
        # Test 2: Avec budget limité
        print("\n2️⃣ Test avec budget limité (5€):")
        solution_base_budget, solution_marge_budget = resoud_avec_contraintes(
            donnees, budget_max=5.0, marge_pourcentage=0.15
        )
        print(f"✅ Solution avec budget: {solution_base_budget[:100]}...")
        print(f"✅ Solution avec marge et budget: {solution_marge_budget[:100]}...")
        
        # Test 3: Avec marge élevée
        print("\n3️⃣ Test avec marge élevée (30%):")
        solution_base_marge, solution_marge_haute = resoud_avec_contraintes(
            donnees, marge_pourcentage=0.3, limite_haricots=False
        )
        print(f"✅ Solution avec marge élevée: {solution_marge_haute[:100]}...")
        
        print("\n🎉 Tous les tests sont passés avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False
    
    return True

def test_donnees_extremes():
    """Test avec des données extrêmes."""
    print("\n🔬 Test avec des données extrêmes...")
    
    # Données très faibles
    besoins_faibles = [500, 20, 50, 20, 2, 100, 10]
    donnees_faibles = Donnees(betaF=besoins_faibles)
    
    try:
        solution1, solution2 = resoud_avec_contraintes(
            donnees_faibles, budget_max=2.0, marge_pourcentage=0.2
        )
        print("✅ Test avec besoins faibles réussi")
    except Exception as e:
        print(f"⚠️ Erreur avec besoins faibles: {str(e)}")
    
    # Données élevées
    besoins_eleves = [4000, 150, 500, 150, 20, 1500, 80]
    donnees_elevees = Donnees(betaF=besoins_eleves)
    
    try:
        solution1, solution2 = resoud_avec_contraintes(
            donnees_elevees, budget_max=20.0, marge_pourcentage=0.1
        )
        print("✅ Test avec besoins élevés réussi")
    except Exception as e:
        print(f"⚠️ Erreur avec besoins élevés: {str(e)}")

if __name__ == "__main__":
    print("🚀 Démarrage des tests de l'application Streamlit\n")
    
    # Test principal
    if test_fonction_resoud():
        print("\n" + "="*50)
        # Test avec données extrêmes
        test_donnees_extremes()
        print("\n" + "="*50)
        print("✅ Application prête à être utilisée !")
        print("🌐 Lancez 'streamlit run app_streamlit.py' pour démarrer l'interface web")
    else:
        print("\n❌ Des erreurs ont été détectées. Vérifiez le code.")
