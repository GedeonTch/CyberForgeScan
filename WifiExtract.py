"""
Module d'extraction des mots de passe WiFi pour CYBER FORGE SCAN
Extrait et sauvegarde les informations des réseaux WiFi enregistrés sur Windows
"""

import os
import sys
import re
from datetime import datetime

def extraire_wifi():
    """
    Extrait les noms et mots de passe des réseaux WiFi enregistrés
    Fonctionne uniquement sur Windows
    """
    print("\n🔍 CYBER FORGE SCAN - Extracteur WiFi")
    print("=" * 50)
    
    # Vérifier si on est sur Windows
    if sys.platform != "win32":
        print("❌ Ce module fonctionne uniquement sur Windows")
        return
    
    try:
        # Récupérer la liste des profils WiFi
        print("\n📡 Récupération des profils WiFi...")
        profiles_output = os.popen("netsh wlan show profiles").read()
        
        if not profiles_output:
            print("❌ Impossible de récupérer les profils WiFi")
            print("💡 Assure-toi d'avoir une carte WiFi active")
            return
        
        # Extraire les noms des profils
        wifi_list = []
        
        for ligne in profiles_output.split("\n"):
            # Cherche "All User Profile" (anglais) ou "Profil Tous les utilisateurs" (français)
            if "All User Profile" in ligne or "Profil Tous les utilisateurs" in ligne:
                # Extrait le nom du WiFi après le ":"
                try:
                    wifi_name = ligne.split(":")[1].strip()
                    if wifi_name:
                        wifi_list.append(wifi_name)
                except IndexError:
                    continue
        
        if not wifi_list:
            print("❌ Aucun profil WiFi trouvé")
            return
        
        print(f"✅ {len(wifi_list)} profil(s) WiFi trouvé(s)\n")
        print("=" * 50)
        
        # Préparer le fichier de sortie
        output_filename = generer_nom_fichier()
        resultats = []
        
        # Pour chaque WiFi, récupérer le mot de passe
        for i, wifi_name in enumerate(wifi_list, 1):
            print(f"\n[{i}/{len(wifi_list)}] Analyse de : {wifi_name}")
            
            try:
                # Commande pour récupérer les détails du profil
                command = f'netsh wlan show profile name="{wifi_name}" key=clear'
                resultat = os.popen(command).read()
                
                # Chercher le mot de passe
                password = extraire_mot_de_passe(resultat)
                
                if password:
                    print(f"   🔑 Mot de passe : {password}")
                    resultats.append({
                        "nom": wifi_name,
                        "password": password
                    })
                else:
                    print(f"   ⚠️  Pas de mot de passe enregistré")
                    resultats.append({
                        "nom": wifi_name,
                        "password": "[Aucun]"
                    })
            
            except Exception as e:
                print(f"   ❌ Erreur : {e}")
                resultats.append({
                    "nom": wifi_name,
                    "password": "[Erreur]"
                })
        
        # Sauvegarder les résultats
        if resultats:
            sauvegarder_resultats(resultats, output_filename)
        
        print("\n" + "=" * 50)
        print("✅ Processus terminé")
        print("=" * 50)
    
    except PermissionError:
        print("\n❌ ERREUR DE PERMISSION")
        print("💡 Lance le script en tant qu'administrateur (clic droit > Exécuter en tant qu'administrateur)")
    
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")


def extraire_mot_de_passe(profil_data: str) -> str:
    """
    Extrait le mot de passe d'un profil WiFi
    
    Args:
        profil_data: Sortie de la commande netsh
    
    Returns:
        Le mot de passe ou None si non trouvé
    """
    # Cherche "Key Content" (anglais) ou "Contenu de la clé" (français)
    for ligne in profil_data.split("\n"):
        ligne_lower = ligne.lower()
        
        if "key content" in ligne_lower or "contenu de la clé" in ligne_lower or "contenu de la cl" in ligne_lower:
            try:
                # Extrait la partie après le ":"
                password = ligne.split(":")[1].strip()
                return password if password else None
            except IndexError:
                continue
    
    return None


def generer_nom_fichier() -> str:
    """
    Génère un nom de fichier unique avec timestamp
    
    Returns:
        Nom du fichier
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"WiFi_Info_{timestamp}.txt"


def sauvegarder_resultats(resultats: list, filename: str):
    """
    Sauvegarde les résultats dans un fichier
    
    Args:
        resultats: Liste des dictionnaires {nom, password}
        filename: Nom du fichier de sortie
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            # En-tête
            f.write("=" * 60 + "\n")
            f.write("CYBER FORGE SCAN - Informations WiFi\n")
            f.write(f"Généré le : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            # Résultats
            for i, info in enumerate(resultats, 1):
                f.write(f"{i}. Réseau : {info['nom']}\n")
                f.write(f"   Mot de passe : {info['password']}\n")
                f.write("-" * 60 + "\n")
            
            # Statistiques
            f.write(f"\nTotal : {len(resultats)} réseau(x) analysé(s)\n")
            avec_mdp = sum(1 for r in resultats if r['password'] not in ['[Aucun]', '[Erreur]'])
            f.write(f"Avec mot de passe : {avec_mdp}\n")
        
        print(f"\n💾 Résultats sauvegardés dans : {filename}")
        print(f"📁 Chemin complet : {os.path.abspath(filename)}")
    
    except Exception as e:
        print(f"\n❌ Erreur lors de la sauvegarde : {e}")


def afficher_menu():
    """Affiche un menu interactif"""
    print("\n🔐 CYBER FORGE SCAN - Extracteur WiFi")
    print("=" * 50)
    print("\n⚠️  AVERTISSEMENT :")
    print("Cet outil est destiné à des fins éducatives uniquement.")
    print("N'utilisez pas cet outil sur des réseaux sans autorisation.\n")
    print("=" * 50)
    
    choix = input("\nVoulez-vous extraire les mots de passe WiFi ? (o/n) : ").strip().lower()
    
    if choix in ['o', 'oui', 'y', 'yes']:
        extraire_wifi()
    else:
        print("\n👋 Opération annulée")


# ============ PROGRAMME PRINCIPAL ============

if __name__ == "__main__":
    afficher_menu()
