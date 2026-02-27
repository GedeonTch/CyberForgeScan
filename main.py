#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CYBER FORGE SCAN - Outil de Cybersécurité
Version: 2.0
Auteur: GedeonTchibanvunya
contact whatsapp: +257 66504165
Description: Suite complète d'outils de sécurité et d'analyse système
"""

import os
import sys
import time
from typing import Optional

# ============================================================================
# CONFIGURATION ET COULEURS POUR L'INTERFACE
# ============================================================================

class Colors:
    """Codes ANSI pour colorer le terminal"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Nettoie l'écran du terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Affiche la bannière principale"""
    clear_screen()
    # Arrière-plan noir et texte vert pour CYBER FORGE SCAN
    print(f"{Colors.GREEN}{Colors.BOLD}")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║                                                                ║")
    print("║            ██████╗██╗   ██╗██████╗ ███████╗██████╗             ║")
    print("║           ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗            ║")
    print("║           ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝            ║")
    print("║           ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗            ║")
    print("║           ╚██████╗   ██║   ██████╔╝███████╗██║  ██║            ║")
    print("║            ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝            ║")
    print("║                                                                ║")
    print("║              FORGE SCAN - Suite de Cybersécurité               ║")
    print("║                        Version 1.0/2026                        ║")
    print("║                        By Gedeon Alias ANONYMOUS               ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    print(f"{Colors.YELLOW}[!] Usage éducatif uniquement - Respectez la loi{Colors.ENDC}\n")

def print_section(title: str):
    """Affiche un titre de section"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'═' * 70}")
    print(f"  {title}")
    print(f"{'═' * 70}{Colors.ENDC}\n")

def print_success(message: str):
    """Affiche un message de succès"""
    print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}")

def print_error(message: str):
    """Affiche un message d'erreur"""
    print(f"{Colors.RED}✗ {message}{Colors.ENDC}")

def print_warning(message: str):
    """Affiche un avertissement"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.ENDC}")

def print_info(message: str):
    """Affiche une information"""
    print(f"{Colors.GREEN}ℹ {message}{Colors.ENDC}")

def pause():
    """Pause avec message"""
    print(f"\n{Colors.YELLOW}Appuyez sur Entrée pour continuer...{Colors.ENDC}")
    input()

# ============================================================================
# IMPORTATION SÉCURISÉE DES MODULES
# ============================================================================

def import_module_safely(module_name: str, display_name: str) -> Optional[object]:
    """
    Importe un module de manière sécurisée
    
    Args:
        module_name: Nom du fichier module (sans .py)
        display_name: Nom d'affichage pour l'utilisateur
    
    Returns:
        Module importé ou None si échec
    """
    try:
        module = __import__(module_name)
        print_success(f"{display_name} chargé")
        return module
    except ImportError as e:
        print_error(f"Impossible de charger {display_name}: {e}")
        return None
    except Exception as e:
        print_error(f"Erreur lors du chargement de {display_name}: {e}")
        return None
    

# ============================================================================
# MENU PRINCIPAL
# ============================================================================

def display_main_menu():
    """Affiche le menu principal"""
    print(f"{Colors.BOLD}{Colors.GREEN}")
    print("┌─────────────────────── MENU PRINCIPAL ───────────────────────┐")
    print("│                                                              │")
    print("│  [1] 🔍  Analyse & Extraction de Données                     │")
    print("│  [2] 🔐  Gestion des Mots de Passe                           │")
    print("│  [3] 📁  Gestion des Fichiers                                │")
    print("│  [4] 🌐  Outils Réseau & Internet                            │")
    print("│  [5] 📥  Téléchargement & Conversion                         │")
    print("│  [6] 🤖  Assistant NOVA IA                                   │")
    print("│  [7] ℹ️   À propos & Aide                                     │")
    print("│  [8] 📝  Feedback                                            │")
    print("│  [0] 🚪  Quitter                                             │")
    print("│                                                              │")
    print("└──────────────────────────────────────────────────────────────┘")
    print(f"{Colors.ENDC}")

# ============================================================================
# SOUS-MENUS
# ============================================================================

def menu_analyse():
    """Menu Analyse & Extraction"""
    while True:
        print_section("🔍 ANALYSE & EXTRACTION DE DONNÉES")
        print(f"{Colors.GREEN}[1]{Colors.ENDC} Analyser un fichier log (emails, IPs, dates)")
        print(f"{Colors.GREEN}[2]{Colors.ENDC} Scanner un dossier")
        print(f"{Colors.GREEN}[3]{Colors.ENDC} Lister les gros fichiers")
        print(f"{Colors.GREEN}[4]{Colors.ENDC} Informations détaillées sur fichiers")
        print(f"{Colors.GREEN}[0]{Colors.ENDC} Retour au menu principal")
        
        choix = input(f"\n{Colors.YELLOW}Votre choix: {Colors.ENDC}").strip()
        
        if choix == "0":
            break
        elif choix == "1":
            try:
                from Analyse import analyser_fichier_log, afficher
                print_info("Module d'analyse de fichiers log")
                chemin = input(f"{Colors.YELLOW}Chemin du fichier à analyser: {Colors.ENDC}").strip()
                if chemin:
                    emails, ips, times, dates,urls= analyser_fichier_log(chemin)
                    afficher(emails, ips, times, dates,urls, chemin)
                    #print(urls)
                    pause()
            except Exception as e:
                print_error(f"Erreur: {e}")
                pause()
        
        elif choix == "2":
            try:
                from Informations import scanner_dossier
                print_info("Scanner de dossier")
                print(f"{Colors.GREEN}╔══════════════════════════════════════════════╗")
                print(f"{Colors.GREEN}║           CYBER  FORGE  SCAN                 ║")
                print(f"{Colors.GREEN}║          FOLDER ANALYSIS  MODULE             ║")
                print(f"{Colors.GREEN}╚══════════════════════════════════════════════╝")
                chemin = input(f"{Colors.YELLOW}Chemin du dossier: {Colors.ENDC}").strip()
                if chemin:
                    scanner_dossier(chemin)
                    pause()
            except Exception as e:
                print_error(f"Erreur: {e}")
                pause()
        
        elif choix == "3":
            try:
                from Informations import lister_gros_fichier
                print_info("Recherche des gros fichiers")
                print(f"{Colors.GREEN}╔══════════════════════════════════════════════╗")
                print(f"{Colors.GREEN}║           CYBER  FORGE  SCAN                 ║")
                print(f"{Colors.GREEN}║          LIST LARGE FILR MODULE              ║")
                print(f"{Colors.GREEN}╚══════════════════════════════════════════════╝")
                chemin = input(f"{Colors.YELLOW}Chemin du dossier: {Colors.ENDC}").strip()
                if chemin:
                    lister_gros_fichier(chemin)
                    pause()
            except Exception as e:
                print_error(f"Erreur: {e}")
                pause()
        
        elif choix == "4":
            try:
                from Informations import informations
                print_info("Analyse détaillée des fichiers")
                print(f"{Colors.GREEN}╔══════════════════════════════════════════════╗")
                print(f"{Colors.GREEN}║           CYBER  FORGE  SCAN                 ║")
                print(f"{Colors.GREEN}║          FILE ANALYSIS  MODULE               ║")
                print(f"{Colors.GREEN}╚══════════════════════════════════════════════╝")
                chemin = input(f"{Colors.YELLOW}Chemin du dossier: {Colors.ENDC}").strip()
                if chemin:
                    informations(chemin)
                    pause()
            except Exception as e:
                print_error(f"Erreur: {e}")
                pause()
        else:
            print_error("Choix invalide")
            time.sleep(1)

def menu_mots_de_passe():
    """Menu Gestion des Mots de Passe"""
    while True:
        print_section("🔐 GESTION DES MOTS DE PASSE")
        print(f"{Colors.GREEN}╔══════════════════════════════════════════════╗")
        print(f"{Colors.GREEN}║           CYBER  FORGE  SCAN                 ║")
        print(f"{Colors.GREEN}║        PASS WORD MANAGEMENT MODULE           ║")
        print(f"{Colors.GREEN}╚══════════════════════════════════════════════╝")
        print(f"{Colors.GREEN}[1]{Colors.ENDC} Générer des mots de passe sécurisés")
        print(f"{Colors.GREEN}[2]{Colors.ENDC} Tester la force d'un mot de passe")
        print(f"{Colors.GREEN}[3]{Colors.ENDC} Générer un mot de passe aléatoire fort")
        print(f"{Colors.GREEN}[4]{Colors.ENDC} Démonstration bruteforce avec 2 options (éducatif)")
        print(f"{Colors.GREEN}[0]{Colors.ENDC} Retour au menu principal")
        
        choix = input(f"\n{Colors.YELLOW}Votre choix: {Colors.ENDC}").strip()
        
        if choix == "0":
            break
        elif choix == "1":
            try:
                from PassWordGenerate import generatePswdWithInfo
                print_info("Générateur de mots de passe personnalisés")
                base = input(f"{Colors.YELLOW}Base du mot de passe (min 6 caractères): {Colors.ENDC}").strip()
                if len(base) >= 6:
                    longueur = int(input(f"{Colors.YELLOW}Caractères à ajouter (min 4): {Colors.ENDC}").strip())
                    if longueur >= 4:
                        generatePswdWithInfo(base, longueur)
                        print_success("Mots de passe sauvegardés dans 'mot de passe.txt'")
                    else:
                        print_error("Longueur minimale: 4 caractères")
                else:
                    print_error("Base minimale: 6 caractères")
                pause()
            except Exception as e:
                print_error(f"Erreur: {e}")
                pause()
        
        elif choix == "2":
            try:
                from PassWordGenerate import passWordTest
                print_info("Test de robustesse d'un mot de passe")
                pwd = input(f"{Colors.YELLOW}Mot de passe à tester: {Colors.ENDC}").strip()
                if pwd:
                    passWordTest(pwd)
                pause()
            except Exception as e:
                print_error(f"Erreur: {e}")
                pause()
        
        elif choix == "3":
            try:
                from PassWordGenerate import genateStrong_WithoutInfo
                print_info("Générateur de mot de passe aléatoire")
                longueur = int(input(f"{Colors.YELLOW}Longueur (min 16): {Colors.ENDC}").strip() or "16")
                pwd = genateStrong_WithoutInfo(longueur)
                print(f"\n{Colors.GREEN}{Colors.BOLD}Mot de passe généré: {pwd}{Colors.ENDC}\n")
                pause()
            except Exception as e:
                print_error(f"Erreur: {e}")
                pause()
        
        elif choix == "4":
            print_warning("⚠️  AVERTISSEMENT - Outil éducatif uniquement!")
            print(f"{Colors.GREEN}╔══════════════════════════════════════════════╗")
            print(f"{Colors.GREEN}║           CYBER  FORGE  SCAN                 ║")
            print(f"{Colors.GREEN}║            BRUTE FORCE MODULE                ║")
            print(f"{Colors.GREEN}╚══════════════════════════════════════════════╝")
            print_warning("Le bruteforce est ILLÉGAL sans autorisation")
            confirm = input(f"{Colors.YELLOW}Continuer? (oui/non): {Colors.ENDC}").strip().lower()
            if confirm in ['oui', 'o', 'yes', 'y']:
                print(f"\nChoisir entre Un BruteForce basique Rapide(1) ou complexe(2) lent effiace")
                choxBurute=int(input(">"))
                if choxBurute==1:
                    print(f"\n{Colors.GREEN}{Colors.BOLD}⚡Ceci est juste une demonstration d'un BruteForce Basique sans dictionnaire")
                    print(f"{Colors.RED}{Colors.BOLD}⚡CYBER FORGE SCAN parcourt tous les caractères pour déviner votre mot de passe\n")
                    try:
                        import time
                        import string
                        
                        total=string.printable
                        found=""
                        motdepasse=input(f"Entrer votre mot de passe:{Colors.ENDC}")
                        print(f"\n{Colors.RED}{Colors.BOLD}DEBUT DU CRACK...\n".center(60))
                        print("\n")
                        for i in range(len(motdepasse)):
                            for letter in total:
                                print(f"{Colors.BLUE}⚡CYBER SCAN essai à la position{i+1} - {letter}",end="\r")
                                time.sleep(0.09)
                                if letter==motdepasse[i]:

                                    found+=letter
                                    print(f"\n{Colors.BLUE}{'='*40}")                                        
                                    print(f"{Colors.GREEN}{Colors.BOLD}- Trouvé!{Colors.RED} {found}")
                                    print(f"{Colors.BLUE}{'='*40}{Colors.ENDC}")
                                    time.sleep(0.6)
                                    break
                        print(f"{Colors.RED}{Colors.BOLD}MOT DE PASSE TROUVE💀:{Colors.GREEN} {found}")
                    except Exception as e:
                        print(f"Une erreu de type  {e} est survenue")
                elif choxBurute==2:
                    try:
                        from bruteforce import buteforce
                        pwd = input(f"{Colors.YELLOW}Mot de passe à tester: {Colors.ENDC}").strip()
                        if pwd:
                            print_info(f"Démarrage de la tentative de craquage...")
                            result = buteforce(pwd)
                            if result:
                                print_success(f"Mot de passe trouvé: {result}")
                        pause()
                    except Exception as e:
                        print_error(f"Erreur: {e}")
                        pause()
        else:
            print_error("Choix invalide")
            time.sleep(1)

def menu_fichiers():
    """Menu Gestion des Fichiers"""
    while True:
        print_section("📁 GESTION DES FICHIERS")
        print(f"{Colors.GREEN}╔══════════════════════════════════════════════╗")
        print(f"{Colors.GREEN}║           CYBER  FORGE  SCAN                 ║")
        print(f"{Colors.GREEN}║          FILE MANAGEMENT MODULE              ║")
        print(f"{Colors.GREEN}╚══════════════════════════════════════════════╝")
        print(f"{Colors.GREEN}[1]{Colors.ENDC} Renommer tous les fichiers d'un dossier")
        print(f"{Colors.GREEN}[2]{Colors.ENDC} Organiser les fichiers par extension")
        print(f"{Colors.GREEN}[3]{Colors.ENDC} Convertir DOCX/TXT vers PDF")
        print(f"{Colors.GREEN}[4]{Colors.ENDC} Conversion en lot (dossier entier)")
        print(f"{Colors.GREEN}[0]{Colors.ENDC} Retour au menu principal")
        
        choix = input(f"\n{Colors.YELLOW}Votre choix: {Colors.ENDC}").strip()
        
        if choix == "0":
            break
        elif choix == "1":
            try:
                from Informations import all_rename
                print_info("Renommage en masse")
                chemin = input(f"{Colors.YELLOW}Chemin du dossier: {Colors.ENDC}").strip()
                nom_base = input(f"{Colors.YELLOW}Nom de base pour les fichiers: {Colors.ENDC}").strip()
                if chemin and nom_base:
                    all_rename(chemin, nom_base)
                    print_success("Fichiers renommés avec succès")
                pause()
            except Exception as e:
                print_error(f"Erreur: {e}")
                pause()
        
        elif choix == "2":
            try:
                from Informations import organiser_fichiers
                print_info("Organisation par extension")
                chemin = input(f"{Colors.YELLOW}Chemin du dossier: {Colors.ENDC}").strip()
                if chemin:
                    organiser_fichiers(chemin)
                    print_success("Fichiers organisés avec succès")
                pause()
            except Exception as e:
                print_error(f"Erreur: {e}")
                pause()
        
        elif choix == "3":
            try:
                from Pdf import convert_to_pdf
                print_info("Conversion vers PDF")
                chemin = input(f"{Colors.YELLOW}Fichier source (.docx ou .txt): {Colors.ENDC}").strip()
                nom_pdf = input(f"{Colors.YELLOW}Nom du PDF (sans extension): {Colors.ENDC}").strip()
                if chemin and nom_pdf:
                    convert_to_pdf(chemin, nom_pdf)
                pause()
            except Exception as e:
                print_error(f"Erreur: {e}")
                pause()
        
        elif choix == "4":
            try:
                from Pdf import batch_convert
                print_info("Conversion en lot")
                dossier = input(f"{Colors.YELLOW}Dossier source: {Colors.ENDC}").strip()
                output = input(f"{Colors.YELLOW}Dossier de sortie (défaut: pdf_output): {Colors.ENDC}").strip() or "pdf_output"
                if dossier:
                    batch_convert(dossier, output)
                pause()
            except Exception as e:
                print_error(f"Erreur: {e}")
                pause()
        else:
            print_error("Choix invalide")
            time.sleep(1)

def menu_reseau():
    """Menu Outils Réseau & Internet"""
    while True:
        print_section("🌐 OUTILS RÉSEAU & INTERNET")
        print(f"{Colors.GREEN}╔══════════════════════════════════════════════╗")
        print(f"{Colors.GREEN}║           CYBER  FORGE  SCAN                 ║")
        print(f"{Colors.GREEN}║         NETWORK SPEED TEST MODULE            ║")
        print(f"{Colors.GREEN}╚══════════════════════════════════════════════╝")
        print(f"{Colors.GREEN}[1]{Colors.ENDC} Tester la vitesse Internet")
        print(f"{Colors.GREEN}[2]{Colors.ENDC} Comparer plusieurs tests de vitesse")
        print(f"{Colors.GREEN}[3]{Colors.ENDC} Extraire les mots de passe WiFi (Windows)")
        print(f"{Colors.GREEN}[0]{Colors.ENDC} Retour au menu principal")
        
        choix = input(f"\n{Colors.YELLOW}Votre choix: {Colors.ENDC}").strip()
        
        if choix == "0":
            break
        elif choix == "1":
            try:
                from connexion import check_internet_speed, display_speed_results
                print_info("Test de vitesse en cours...")
                speed = check_internet_speed()
                display_speed_results(speed)
                pause()
            except Exception as e:
                print_error(f"Erreur: {e}")
                pause()
        
        elif choix == "2":
            try:
                from connexion import compare_speeds
                print_info("Comparaison de vitesses")
                compare_speeds()
                pause()
            except Exception as e:
                print_error(f"Erreur: {e}")
                pause()
        
        elif choix == "3":
            if sys.platform != "win32":
                print_error("Cette fonction nécessite Windows")
                pause()
                continue
            
            print_warning("⚠️  Cet outil nécessite des droits administrateur")
            print_warning("⚠️  Usage légal uniquement - Vos propres réseaux")
            print(f"{Colors.GREEN}╔══════════════════════════════════════════════╗")
            print(f"{Colors.GREEN}║           CYBER  FORGE  SCAN                 ║")
            print(f"{Colors.GREEN}║          WIFI EXTACTION MODULE               ║")
            print(f"{Colors.GREEN}╚══════════════════════════════════════════════╝")
            confirm = input(f"{Colors.YELLOW}Continuer? (oui/non): {Colors.ENDC}").strip().lower()
            if confirm in ['oui', 'o', 'yes', 'y']:
                try:
                    from WifiExtract import extraire_wifi
                    extraire_wifi()
                    pause()
                except Exception as e:
                    print_error(f"Erreur: {e}")
                    pause()
        else:
            print_error("Choix invalide")
            time.sleep(1)

def menu_telechargement():
    """Menu Téléchargement & Conversion"""
    while True:
        print_section("📥 TÉLÉCHARGEMENT & CONVERSION")
        print(f"{Colors.GREEN}╔══════════════════════════════════════════════╗")
        print(f"{Colors.GREEN}║           CYBER  FORGE  SCAN                 ║")
        print(f"{Colors.GREEN}║             DOWNLOAD MODULE                  ║")
        print(f"{Colors.GREEN}╚══════════════════════════════════════════════╝")
        print(f"{Colors.GREEN}[1]{Colors.ENDC} Télécharger une vidéo YouTube")
        print(f"{Colors.GREEN}[2]{Colors.ENDC} Télécharger l'audio uniquement")
        print(f"{Colors.GREEN}[3]{Colors.ENDC} Voir les infos d'une vidéo")
        print(f"{Colors.GREEN}[4]{Colors.ENDC} Enregistrer l'écran")
        print(f"{Colors.GREEN}[0]{Colors.ENDC} Retour au menu principal")
        
        choix = input(f"\n{Colors.YELLOW}Votre choix: {Colors.ENDC}").strip()
        
        if choix == "0":
            break
        elif choix in ["1", "2", "3"]:
            try:
                from Youtube import YouTubeDownloader
                downloader = YouTubeDownloader()
                url = input(f"{Colors.YELLOW}URL YouTube: {Colors.ENDC}").strip()
                
                if not url:
                    print_error("URL vide")
                    pause()
                    continue
                
                if choix == "1":
                    downloader.download_video(url)
                elif choix == "2":
                    downloader.download_audio(url)
                elif choix == "3":
                    info = downloader.get_video_info(url)
                    print_section("INFORMATIONS VIDÉO")
                    for key, value in info.items():
                        print(f"{Colors.GREEN}{key.capitalize()}{Colors.ENDC}: {value}")
                
                pause()
            except Exception as e:
                print_error(f"Erreur: {e}")
                pause()
        
        elif choix == "4":
            try:
                from ScreenRecord import demo_screen_recorder
                demo_screen_recorder()
            except Exception as e:
                print_error(f"Erreur: {e}")
                pause()
        else:
            print_error("Choix invalide")
            time.sleep(1)

def menu_ia():
    """Menu Assistant IA"""
    while True:
        print(f"{Colors.GREEN}╔══════════════════════════════════════════════╗")
        print(f"{Colors.GREEN}║           CYBER  FORGE  SCAN                 ║")
        print(f"{Colors.GREEN}║            ASSISTANT NOVA IA                 ║")
        print(f"{Colors.GREEN}╚══════════════════════════════════════════════╝")
        print_section("🤖 NOVA IA(ASSISTANT)")
        print(f"{Colors.GREEN}[1]{Colors.ENDC} Démarrer l'assistant NOVA IA (Ollama)")
        print(f"{Colors.GREEN}[2]{Colors.ENDC} À propos de NOVA")
        print(f"{Colors.GREEN}[0]{Colors.ENDC} Retour au menu principal")
        
        choix = input(f"\n{Colors.YELLOW}Votre choix: {Colors.ENDC}").strip()
        
        if choix == "0":
            break
        elif choix == "1":
            try:
                from ChatBot import demo_assistant
                demo_assistant()
            except Exception as e:
                print_error(f"Erreur: {e}")
                print_info("Assurez-vous qu'Ollama est installé et en cours d'exécution")
                print_info("Installer: https://ollama.ai")
                pause()
        
        elif choix == "2":
            print_section("À PROPOS DE L'ASSISTANT NOVA IA")
            print(f"{Colors.GREEN}L'assistant NOVA IA utilise Ollama pour fournir:")
            print("  • Réponses aux questions sur la cybersécurité")
            print("  • Aide sur l'utilisation des outils")
            print("  • Support conversationnel")
            print(f"\n{Colors.YELLOW}Prérequis:{Colors.ENDC}")
            print("  1. Installer Ollama: https://ollama.ai")
            print("  2. Télécharger un modèle: ollama pull phi3:mini")
            print("  3. Lancer le serveur: ollama serve")
            pause()
        else:
            print_error("Choix invalide")
            time.sleep(1)
def commentaire():
    "Laisser un avis"
    print_section("LAISSER VOTRE COMMENTAIRE:")
    try:
        from feedback import collecter_feedback
       
        collecter_feedback()
    except Exception as e:
        print_error(f"Erreur: {e}") 

def menu_aide():
    """Menu À propos & Aide"""
    print_section("ℹ️  À PROPOS DE CYBER FORGE SCAN")
    
    print(f"{Colors.BOLD}Version:{Colors.ENDC} 1.0")
    print(f"{Colors.BOLD}Auteur:{Colors.ENDC} Gedeon Tchibanvunya")
    print(f"{Colors.BOLD}Contact:{Colors.ENDC} tchibanvunyagedeon@gmail.com/whatsApp:+257 66504165")
    print(f"{Colors.BOLD}Description:{Colors.ENDC} Suite complète d'outils d'analyse de cybersécurité\n")
    
    print(f"{Colors.CYAN}{Colors.BOLD}MODULES DISPONIBLES:{Colors.ENDC}")
    print(f"{Colors.GREEN}✓{Colors.ENDC} Analyse de fichiers logs")
    print(f"{Colors.GREEN}✓{Colors.ENDC} Générateur de mots de passe")
    print(f"{Colors.GREEN}✓{Colors.ENDC} Gestion de fichiers")
    print(f"{Colors.GREEN}✓{Colors.ENDC} Test de vitesse Internet")
    print(f"{Colors.GREEN}✓{Colors.ENDC} Extraction WiFi (Windows)")
    print(f"{Colors.GREEN}✓{Colors.ENDC} Téléchargement YouTube")
    print(f"{Colors.GREEN}✓{Colors.ENDC} Conversion PDF")
    print(f"{Colors.GREEN}✓{Colors.ENDC} Enregistrement d'écran")
    print(f"{Colors.GREEN}✓{Colors.ENDC} Assistant NOVA IA (Ollama)")
    print(f"{Colors.GREEN}✓{Colors.ENDC} FEEDBACK (VOTRE AVIS)")
    
    print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  AVERTISSEMENT LÉGAL:{Colors.ENDC}")
    print("Cet outil est destiné à des fins éducatives uniquement.")
    print("L'utilisation malveillante est strictement interdite et illégale.")
    print("L'auteur décline toute responsabilité en cas de mauvaise utilisation.")
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}PRÉREQUIS:{Colors.ENDC}")
    print("• Python 3.14.0+")
    print("• Modules: voir requirements.txt")
    print("• Ollama (optionnel pour l'IA)")
    
    pause()
# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    """Fonction principale du programme"""
    
    # Vérification de la version Python
    if sys.version_info < (3, 7):
        print_error("Python 3.7 ou supérieur requis")
        sys.exit(1)
    
    # Boucle principale
    while True:
        print_banner()
        time.sleep(2)
        #progres()
        display_main_menu()
        
        choix = input(f"{Colors.YELLOW}{Colors.BOLD}Votre choix: {Colors.ENDC}").strip()
        
        if choix == "0":
            print_section("👋 AU REVOIR")
            print(f"{Colors.GREEN}Merci d'avoir utilisé CYBER FORGE SCAN{Colors.ENDC}")
            print(f"{Colors.YELLOW}Restez en sécurité! 🔐{Colors.ENDC}\n")
            sys.exit(0)
        
        elif choix == "1":
            menu_analyse()
        
        elif choix == "2":
            menu_mots_de_passe()
        
        elif choix == "3":
            menu_fichiers()
        
        elif choix == "4":
            menu_reseau()
        
        elif choix == "5":
            menu_telechargement()
        
        elif choix == "6":
            menu_ia()
        
        elif choix == "7":
            menu_aide()
            
        elif choix== "8":
            commentaire()
        else:
            print_error("Choix invalide. Veuillez réessayer.")
            time.sleep(1)

# ============================================================================
# POINT D'ENTRÉE
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Programme interrompu par l'utilisateur{Colors.ENDC}")
        print(f"{Colors.GREEN}Au revoir!{Colors.ENDC}\n")
        sys.exit(0)
    except Exception as e:
        print_error(f"Erreur critique: {e}")
        sys.exit(1)

