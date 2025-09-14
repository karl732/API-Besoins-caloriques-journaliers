"""
Script de lancement pour l'application Streamlit d'optimisation des repas.
"""

import subprocess
import sys
import os
import time

def verifier_dependances():
    """Vérifie que toutes les dépendances sont installées."""
    print("🔍 Vérification des dépendances...")
    
    dependances = ['streamlit', 'pandas', 'numpy', 'scipy']
    manquantes = []
    
    for dep in dependances:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep}")
            manquantes.append(dep)
    
    if manquantes:
        print(f"\n⚠️ Dépendances manquantes: {', '.join(manquantes)}")
        print("Installez-les avec: pip install " + " ".join(manquantes))
        return False
    
    print("✅ Toutes les dépendances sont installées !")
    return True

def verifier_fichiers():
    """Vérifie que tous les fichiers nécessaires existent."""
    print("\n📁 Vérification des fichiers...")
    
    fichiers_requis = [
        'app_streamlit.py',
        'final/lib_resolution.py',
        'final/data.py',
        'final/Aliments.csv'
    ]
    
    manquants = []
    
    for fichier in fichiers_requis:
        if os.path.exists(fichier):
            print(f"✅ {fichier}")
        else:
            print(f"❌ {fichier}")
            manquants.append(fichier)
    
    if manquants:
        print(f"\n⚠️ Fichiers manquants: {', '.join(manquants)}")
        return False
    
    print("✅ Tous les fichiers sont présents !")
    return True

def lancer_application():
    """Lance l'application Streamlit."""
    print("\n🚀 Lancement de l'application Streamlit...")
    print("📱 L'application s'ouvrira dans votre navigateur à l'adresse: http://localhost:8501")
    print("🛑 Pour arrêter l'application, appuyez sur Ctrl+C")
    print("-" * 60)
    
    try:
        # Lancer Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app_streamlit.py"], 
                      check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Application arrêtée par l'utilisateur.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur lors du lancement: {e}")
        print("💡 Essayez de lancer manuellement: streamlit run app_streamlit.py")
    except FileNotFoundError:
        print("\n❌ Streamlit n'est pas installé ou accessible.")
        print("💡 Installez Streamlit avec: pip install streamlit")

def main():
    """Fonction principale."""
    print("🍽️ Optimiseur de Repas Journaliers - Lancement")
    print("=" * 50)
    
    # Vérifications
    if not verifier_dependances():
        return
    
    if not verifier_fichiers():
        return
    
    # Test rapide
    print("\n🧪 Test rapide de l'application...")
    try:
        from final.data import Donnees
        from final.lib_resolution import resoud_avec_contraintes
        
        # Test simple
        donnees_test = Donnees(betaF=[2000, 75, 225, 90, 9, 800, 45])
        print("✅ Modules importés et fonctionnels !")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return
    
    print("\n" + "=" * 50)
    
    # Lancement
    reponse = input("🚀 Voulez-vous lancer l'application maintenant ? (o/n): ").lower().strip()
    
    if reponse in ['o', 'oui', 'y', 'yes', '']:
        lancer_application()
    else:
        print("\n📋 Pour lancer l'application manuellement:")
        print("   streamlit run app_streamlit.py")
        print("\n📖 Ou utilisez ce script:")
        print("   python lancer_app.py")

if __name__ == "__main__":
    main()
