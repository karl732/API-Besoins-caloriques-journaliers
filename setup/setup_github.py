"""
Script pour configurer et pousser le projet sur GitHub.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description=""):
    """Exécute une commande et affiche le résultat."""
    print(f"🔄 {description}")
    print(f"   Commande: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Succès")
            if result.stdout.strip():
                print(f"   Sortie: {result.stdout.strip()}")
        else:
            print(f"❌ {description} - Erreur")
            print(f"   Erreur: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {str(e)}")
        return False
    
    return True

def check_git_installed():
    """Vérifie que Git est installé."""
    return run_command("git --version", "Vérification de Git")

def init_git_repo():
    """Initialise le repository Git."""
    if os.path.exists(".git"):
        print("📁 Repository Git déjà initialisé")
        return True
    return run_command("git init", "Initialisation du repository Git")

def create_gitignore_if_missing():
    """Crée un .gitignore basique s'il n'existe pas."""
    if not os.path.exists(".gitignore"):
        print("📝 Création d'un .gitignore basique...")
        with open(".gitignore", "w") as f:
            f.write("__pycache__/\n*.pyc\n.env\nvenv/\n.vscode/\n.streamlit/\n")
        return True
    else:
        print("✅ .gitignore existe déjà")
        return True

def add_files():
    """Ajoute tous les fichiers au staging."""
    return run_command("git add .", "Ajout des fichiers au staging")

def commit_initial():
    """Fait le commit initial."""
    return run_command(
        'git commit -m "feat: initial commit - Optimiseur de Repas Journaliers avec interface Streamlit"',
        "Commit initial"
    )

def check_remote():
    """Vérifie si une remote origin existe."""
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    return "origin" in result.stdout

def add_remote(repo_url):
    """Ajoute la remote origin."""
    return run_command(f"git remote add origin {repo_url}", f"Ajout de la remote {repo_url}")

def push_to_github():
    """Pousse vers GitHub."""
    return run_command("git push -u origin main", "Push vers GitHub")

def create_main_branch():
    """Crée et bascule vers la branche main."""
    run_command("git branch -M main", "Création de la branche main")

def display_project_status():
    """Affiche le statut du projet."""
    print("\n" + "="*60)
    print("📊 STATUT DU PROJET")
    print("="*60)
    
    # Compter les fichiers
    python_files = list(Path(".").rglob("*.py"))
    md_files = list(Path(".").rglob("*.md"))
    
    print(f"📁 Fichiers Python: {len(python_files)}")
    print(f"📝 Fichiers Markdown: {len(md_files)}")
    config_files = list(Path('.').glob('*.toml')) + list(Path('.').glob('*.txt'))
    print(f"📋 Fichiers de configuration: {len(config_files)}")
    
    # Vérifier les fichiers importants
    important_files = [
        "README.md", "LICENSE", "CONTRIBUTING.md", 
        ".gitignore", "requirements.txt", "app_streamlit.py"
    ]
    
    print(f"\n✅ Fichiers importants présents:")
    for file in important_files:
        status = "✅" if os.path.exists(file) else "❌"
        print(f"   {status} {file}")

def main():
    """Fonction principale."""
    print("🚀 CONFIGURATION GITHUB - Optimiseur de Repas Journaliers")
    print("="*60)
    
    # Vérifications préliminaires
    if not check_git_installed():
        print("❌ Git n'est pas installé. Veuillez l'installer d'abord.")
        return
    
    # Afficher le statut du projet
    display_project_status()
    
    print("\n" + "="*60)
    print("🔧 CONFIGURATION GIT")
    print("="*60)
    
    # Configuration Git
    if not init_git_repo():
        return
    
    create_gitignore_if_missing()
    create_main_branch()
    
    # Demander l'URL du repository
    print("\n📋 CONFIGURATION GITHUB")
    print("-"*30)
    print("1. Créez d'abord un repository sur GitHub")
    print("2. Copiez l'URL HTTPS ou SSH du repository")
    print("   Exemple: https://github.com/votre-username/optimiseur-repas-journaliers.git")
    
    repo_url = input("\n🔗 URL de votre repository GitHub: ").strip()
    
    if not repo_url:
        print("❌ URL du repository requise")
        return
    
    # Ajouter les fichiers et commiter
    if not add_files():
        return
    
    if not commit_initial():
        return
    
    # Configurer la remote si nécessaire
    if not check_remote():
        if not add_remote(repo_url):
            return
    else:
        print("✅ Remote origin déjà configurée")
    
    # Push vers GitHub
    print(f"\n🚀 Push vers GitHub...")
    if push_to_github():
        print(f"\n🎉 SUCCÈS ! Votre projet est maintenant sur GitHub !")
        print(f"🌐 Visitez: {repo_url.replace('.git', '')}")
        print(f"📱 Streamlit App: streamlit run app_streamlit.py")
        
        print(f"\n📋 Prochaines étapes:")
        print(f"   1. Visitez votre repository sur GitHub")
        print(f"   2. Ajoutez une description attractive")
        print(f"   3. Ajoutez des topics/tags: python, streamlit, optimization, nutrition")
        print(f"   4. Activez GitHub Pages si souhaité")
        print(f"   5. Invitez des collaborateurs si nécessaire")
        
    else:
        print(f"\n❌ Erreur lors du push. Vérifiez:")
        print(f"   - Que le repository existe sur GitHub")
        print(f"   - Que vous avez les droits d'écriture")
        print(f"   - Que l'URL est correcte")

if __name__ == "__main__":
    main()
