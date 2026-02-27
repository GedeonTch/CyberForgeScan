#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module d'Analyse de Fichiers Log - CYBER FORGE SCAN
Extrait et analyse les données sensibles depuis les fichiers log
""" 

import os
import re
from datetime import datetime
from typing import Tuple, List

# ============================================================================
# CONFIGURATION
# ============================================================================

# Mots-clés sensibles à détecter
MOTS_SENSIBLES = [
    "error", "permission", "admin", "root", "hack", 
    "access", "denied", "granted", "fail", "failed",
    "warning", "critical", "alert", "breach", "attack",
    "unauthorized", "forbidden", "exception","api_key",
    "crypt","token","auth","credential","secret","ip",
    "password","motdepasse","select","instert","waen","fatal",
    "panic","timeout","refused","invalid","500","502","503","404","oom",
    "segfault","login","killed","token","brute force","sql","401"
]


# Extensions de fichiers supportées
EXTENSIONS_SUPPORTEES = (".txt", ".log", ".conf", ".cfg")

# Fichier de sortie par défaut
FICHIER_SORTIE = "Extraction_Analyse.txt"

# ============================================================================
# COULEURS POUR AFFICHAGE (compatible avec main.py)
# ============================================================================

class Colors:
    """Codes ANSI pour colorer le terminal"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

# ============================================================================
# FONCTIONS D'EXTRACTION
# ============================================================================

def extraire_info_ligne(ligne: str) -> Tuple[List[str], List[str], List[str], List[str], List[str]]:
    """
    Extrait les informations structurées d'une ligne de log
    
    Args:
        ligne: Ligne de texte à analyser
    
    Returns:
        Tuple (emails, ips, heures, dates, liens)
    """
    # Extraction des emails (RFC 5322 simplifié)
    emails = re.findall(
        r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b", 
        ligne
    )
    
    # Extraction des adresses IPv4
    ips = re.findall(
        r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", 
        ligne
    )
    
    # Extraction des heures (formats: HH:MM, HH:MM:SS, avec AM/PM optionnel)
    heures = re.findall(
        r"\b[0-2]?[0-9]:[0-5][0-9](?::[0-5][0-9])?(?:\s?(?:AM|PM|am|pm))?\b", 
        ligne
    )
    
    # Extraction des dates (formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD)
    dates = re.findall(
        r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})\b", 
        ligne
    )

    #Extractions des liens(http//https//w.w.w...)
    urls= re.findall(
        r"https?://(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)",
        ligne
    )
    
    return emails, ips, heures, dates, urls

def valider_ip(ip: str) -> bool:
    """
    Valide qu'une adresse IP est dans la plage correcte (0-255)
    
    Args:
        ip: Adresse IP à valider
    
    Returns:
        True si valide, False sinon
    """
    octets = ip.split('.')
    return all(0 <= int(octet) <= 255 for octet in octets)

# ============================================================================
# FONCTION PRINCIPALE D'ANALYSE
# ============================================================================

def analyser_fichier_log(chemin: str, mots_sensibles: List[str] = None) -> Tuple[List[str], List[str], List[str], List[str],List[str]]:
    """
    Analyse un fichier log et extrait les données sensibles
    
    Args:
        chemin: Chemin du fichier à analyser
        mots_sensibles: Liste de mots-clés à détecter (optionnel)
    
    Returns:
        Tuple (emails, ips, heures, dates) - listes déduplicatées
    """
    # Utiliser les mots sensibles par défaut si non fournis
    if mots_sensibles is None:
        mots_sensibles = MOTS_SENSIBLES
    
    # Initialisation des listes
    emails, ips, heures, dates, urls = set(), set(), set(), set(), set()
    alertes = []
    
    # Vérification de l'existence du fichier
    if not os.path.exists(chemin):
        print(f"{Colors.RED}✗⚠ Erreur: Fichier introuvable⚠️: {chemin}{Colors.ENDC}")
        return [], [], [], [], []
    
    # Vérification de l'extension
    if not chemin.lower().endswith(EXTENSIONS_SUPPORTEES):
        print(f"{Colors.YELLOW}⚠ Avertissement: Extension non standard. Formats recommandés: {EXTENSIONS_SUPPORTEES}{Colors.ENDC}")
    
    print(f"{Colors.GREEN}📂✅⚡CyberForgeScan⚡Analyse Votre fichier: {chemin}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 70}{Colors.ENDC}\n")
    
    ligne_num = 0
    
    try:
        # Tentative de lecture avec plusieurs encodages
        encodages = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        fichier_ouvert = False
        
        for encodage in encodages:
            try:
                with open(chemin, "r", encoding=encodage) as f:
                    fichier_ouvert = True
                    
                    for ligne in f:
                        ligne_num += 1
                        ligne = ligne.strip()
                        
                        if not ligne:  # Ignorer les lignes vides
                            continue
                        
                        # Extraction des données
                        e, i, h, d,u = extraire_info_ligne(ligne)
                        
                        # Ajout aux ensembles (déduplique automatiquement)
                        emails.update(e)
                        heures.update(h)
                        dates.update(d)
                        urls.update(u)
                        
                        # Validation et ajout des IPs
                        for ip in i:
                            if valider_ip(ip):
                                ips.add(ip)
                        
                        # Détection de mots sensibles
                        ligne_lower = ligne.lower()
                        for mot in mots_sensibles:
                            if mot.lower() in ligne_lower:
                                alerte = {
                                    'ligne': ligne_num,
                                    'mot_cle': mot,
                                    'contenu': ligne[:100]  # Limiter à 100 caractères
                                }
                                alertes.append(alerte)
                                
                                # Affichage de l'alerte
                                print(f"{Colors.RED}🚨 ALERTE - Ligne {ligne_num}{Colors.ENDC}")
                                print(f"{Colors.YELLOW}   Mot-clé: {mot}{Colors.ENDC}")
                                print(f"{Colors.CYAN}   Contenu: {ligne[:100]}{'...' if len(ligne) > 100 else ''}{Colors.ENDC}")
                                print(f"{Colors.CYAN}   {'─' * 70}{Colors.ENDC}\n")
                    
                    break  # Sortir de la boucle si la lecture a réussi
                    
            except UnicodeDecodeError:
                if encodage == encodages[-1]:  # Dernier encodage tenté
                    raise
                continue  # Essayer l'encodage suivant
        
        if not fichier_ouvert:
            raise Exception("Impossible de lire le fichier avec les encodages supportés")
        
        # Conversion des ensembles en listes triées
        emails_list = sorted(list(emails))
        ips_list = sorted(list(ips))
        heures_list = sorted(list(heures))
        dates_list = sorted(list(dates))
        liens_list= sorted(list(urls))
        
        # Sauvegarde des résultats
        sauvegarder_resultats(chemin, emails_list, ips_list, heures_list, dates_list,liens_list, alertes)
        
        # Affichage du résumé
        print(f"\n{Colors.GREEN}✅ Analyse terminée!{Colors.ENDC}")
        print(f"{Colors.CYAN}{'═' * 70}{Colors.ENDC}")
        print(f"{Colors.BOLD}📊 STATISTIQUES:{Colors.ENDC}")
        print(f"   • Lignes analysées: {ligne_num}")
        print(f"   • Emails trouvés: {len(emails_list)}")
        print(f"   • IPs trouvées: {len(ips_list)}")
        print(f"   • Heures trouvées: {len(heures_list)}")
        print(f"   • Dates trouvées: {len(dates_list)}")
        print(f"   • Liens trouvés: {len(liens_list)}")
        print(f"   • Alertes: {len(alertes)}")
        print(f"{Colors.CYAN}{'═' * 70}{Colors.ENDC}\n")
        print(f"{Colors.GREEN}💾 Résultats sauvegardés dans: {FICHIER_SORTIE}{Colors.ENDC}\n")
        
        return emails_list, ips_list, heures_list, dates_list, liens_list
        
    except FileNotFoundError:
        print(f"{Colors.RED}✗ Erreur: Fichier introuvable: {chemin}{Colors.ENDC}")
        return [], [], [], [], []
    
    except PermissionError:
        print(f"{Colors.RED}✗ Erreur: Permission refusée pour lire: {chemin}{Colors.ENDC}")
        return [], [], [], [], []
    
    except Exception as e:
        print(f"{Colors.RED}✗ Erreur inattendue: {type(e).__name__} - {e}{Colors.ENDC}")
        return [], [], [], [], []

# ============================================================================
# SAUVEGARDE DES RÉSULTATS
# ============================================================================

def sauvegarder_resultats(chemin_source: str, emails: List[str], ips: List[str], 
                          heures: List[str], dates: List[str],urls: List[str], alertes: List[dict]) -> None:
    """
    Sauvegarde les résultats de l'analyse dans un fichier
    
    Args:
        chemin_source: Chemin du fichier analysé
        emails: Liste des emails trouvés
        ips: Liste des IPs trouvées
        heures: Liste des heures trouvées
        dates: Liste des dates trouvées
        alertes: Liste des alertes détectées
    """
    try:
        with open(FICHIER_SORTIE, "w", encoding="utf-8") as f:
            # En-tête
            f.write("=" * 80 + "\n")
            f.write("CYBER FORGE SCAN - RAPPORT D'ANALYSE DE LOG\n")
            f.write("=" * 80 + "\n\n")
            
            # Informations sur le fichier analysé
            f.write(f"📂 Fichier analysé: {chemin_source}\n")
            f.write(f"📅 Date d'analyse: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"📊 Taille du fichier: {os.path.getsize(chemin_source)} octets\n")
            f.write("\n" + "-" * 80 + "\n\n")
            
            # Emails
            f.write(f"📧 EMAILS TROUVÉS ({len(emails)}):\n")
            f.write("-" * 80 + "\n")
            if emails:
                for i, email in enumerate(emails, 1):
                    f.write(f"{i:3d}. {email}\n")
            else:
                f.write("Aucun email trouvé.\n")
            f.write("\n")
            
            # IPs
            f.write(f"🌐 ADRESSES IP TROUVÉES ({len(ips)}):\n")
            f.write("-" * 80 + "\n")
            if ips:
                for i, ip in enumerate(ips, 1):
                    f.write(f"{i:3d}. {ip}\n")
            else:
                f.write("Aucune adresse IP trouvée.\n")
            f.write("\n")
            
            # Heures
            f.write(f"🕐 HEURES TROUVÉES ({len(heures)}):\n")
            f.write("-" * 80 + "\n")
            if heures:
                for i, heure in enumerate(heures, 1):
                    f.write(f"{i:3d}. {heure}\n")
            else:
                f.write("Aucune heure trouvée.\n")
            f.write("\n")
            
            # Dates
            f.write(f"📅 DATES TROUVÉES ({len(dates)}):\n")
            f.write("-" * 80 + "\n")
            if dates:
                for i, date in enumerate(dates, 1):
                    f.write(f"{i:3d}. {date}\n")
            else:
                f.write("Aucune date trouvée.\n")
            f.write("\n")

            #Liens
            f.write(f"🔗 LIENS TROUVÉS ({len(urls)}):\n")
            f.write("-" * 80 + "\n")
            if urls:
                for i, url in enumerate(urls, 1):
                    f.write(f"{i:3d}. {url}\n")
            else:
                f.write("Aucun lien trouvé.\n")
            f.write("\n")
            
            # Alertes
            f.write(f"🚨 ALERTES DE SÉCURITÉ ({len(alertes)}):\n")
            f.write("-" * 80 + "\n")
            if alertes:
                for i, alerte in enumerate(alertes, 1):
                    f.write(f"\n{i}. Ligne {alerte['ligne']} - Mot-clé: {alerte['mot_cle']}\n")
                    f.write(f"   Contenu: {alerte['contenu']}\n")
            else:
                f.write("Aucune alerte détectée.\n")
            
            # Pied de page
            f.write("\n" + "=" * 80 + "\n")
            f.write("FIN DU RAPPORT\n")
            f.write("=" * 80 + "\n")
            
    except Exception as e:
        print(f"{Colors.RED}✗ Erreur lors de la sauvegarde: {e}{Colors.ENDC}")

# ============================================================================
# FONCTION D'AFFICHAGE
# ============================================================================

def afficher(emails: List[str], ips: List[str], heures: List[str], dates: List[str],urls: List[str], fichier: str = None) -> None:
    """
    Affiche les résultats de l'analyse de manière formatée
    
    Args:
        emails: Liste des emails trouvés
        ips: Liste des IPs trouvées
        heures: Liste des heures trouvées
        dates: Liste des dates trouvées
        fichier: Nom du fichier analysé (optionnel)
    """
    print(f"{Colors.GREEN}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║      CYBER FORGE SCAN - Analyseur de Fichiers Log        ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")

    if fichier:
        print(f"\n{Colors.BOLD}{Colors.GREEN}{'=' * 70}")
        print(f"RÉSULTATS DE L'ANALYSE - {fichier}")
        print(f"{'=' * 70}{Colors.ENDC}\n")
    else:
        print(f"\n{Colors.BOLD}{Colors.GREEN}{'=' * 70}")
        print("RÉSULTATS DE L'ANALYSE")
        print(f"{'=' * 70}{Colors.ENDC}\n")
    """Affiche les résultats de l'analyse de manière formatée
    
    Args:
        emails: Liste des emails trouvés
        ips: Liste des IPs trouvées
        heures: Liste des heures trouvées
        dates: Liste des dates trouvées
    """
    if fichier:
        print(f"\n{Colors.BOLD}{Colors.GREEN}{'=' * 70}")
        print(f"RÉSULTATS DE L'ANALYSE - {fichier}")
        print(f"{'=' * 70}{Colors.ENDC}\n")
    else:
        print(f"\n{Colors.BOLD}{Colors.GREEN}{'=' * 70}")
        print("RÉSULTATS DE L'ANALYSE")
    print("RÉSULTATS DE L'ANALYSE")
    print(f"{'═' * 70}{Colors.ENDC}\n")
    
    # Emails
    if emails:
        print(f"{Colors.GREEN}📧 Emails trouvés ({len(emails)}):{Colors.ENDC}")
        for i, email in enumerate(emails, 1):
            print(f"   {i:2d}. {email}")
    else:
        print(f"{Colors.YELLOW}📧 Aucun email trouvé{Colors.ENDC}")
    print()
    
    # IPs
    if ips:
        print(f"{Colors.GREEN}🌐 Adresses IP trouvées ({len(ips)}):{Colors.ENDC}")
        for i, ip in enumerate(ips, 1):
            print(f"   {i:2d}. {ip}")
    else:
        print(f"{Colors.YELLOW}🌐 Aucune adresse IP trouvée{Colors.ENDC}")
    print()
    
    # Heures
    if heures:
        print(f"{Colors.GREEN}🕐 Heures trouvées ({len(heures)}):{Colors.ENDC}")
        for i, heure in enumerate(heures, 1):
            print(f"   {i:2d}. {heure}")
    else:
        print(f"{Colors.YELLOW}🕐 Aucune heure trouvée{Colors.ENDC}")
    print()
    
    # Dates
    if dates:
        print(f"{Colors.GREEN}📅 Dates trouvées ({len(dates)}):{Colors.ENDC}")
        for i, date in enumerate(dates, 1):
            print(f"   {i:2d}. {date}")
    else:
        print(f"{Colors.YELLOW}📅 Aucune date trouvée{Colors.ENDC}")
    print()

    #Liens
    if urls:
        print(f"{Colors.GREEN}🔗 Liens trouvés ({len(urls)}):{Colors.ENDC}")
        for i, url in enumerate(urls, 1):
            print(f"   {i:2d}. {url}")
    else:
        print(f"{Colors.YELLOW}📅 Aucune lien trouvé trouvée{Colors.ENDC}")
    
    # Résumé final
    print(f"{Colors.BOLD}{Colors.GREEN}{'✅' * 35}")
    print("RÉSUMÉ FINAL:")
    print(f"  • Emails trouvés: {len(emails)}")
    print(f"  • Adresses IP trouvées: {len(ips)}")
    print(f"  • Heures trouvées: {len(heures)}")
    print(f"  • Dates trouvées: {len(dates)}")
    print(f"  • Liens trouvés: {len(urls)}")
    print(f"{'✅' * 35}{Colors.ENDC}\n")

# ============================================================================
# FONCTION PRINCIPALE (pour tests standalone)
# ============================================================================

def main():
    """Fonction principale pour exécution standalone"""
    print(f"{Colors.GREEN}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║      CYBER FORGE SCAN - Analyseur de Fichiers Log        ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")
    print("\n")
    print(f"{Colors.GREEN}Pour copier le chemin du fichier ou du dossier faites un clic droit sur le fichier{Colors.ENDC}")
    print(f"{Colors.GREEN}En suite sélectionnez copier le chemin. ou faites CTRL+SHIFT+C sur le fichier/dossier{Colors.ENDC}")
    chemin = input(f"{Colors.YELLOW}Entrez le chemin du fichier à analyser: {Colors.ENDC}").strip()

    
    if not chemin:
        print(f"{Colors.RED}✗ Erreur: Chemin vide{Colors.ENDC}")
        return
    
    # Supprimer les guillemets si présents
    chemin = chemin.strip('"').strip("'")
    
    # Analyse du fichier
    emails, ips, heures, dates, urls = analyser_fichier_log(chemin)
    
    # Affichage des résultats
    if emails or ips or heures or dates or urls:
        afficher(emails, ips, heures, dates, urls)
    else:
        print(f"{Colors.YELLOW}⚠ Aucune donnée extraite du fichier{Colors.ENDC}")

# ============================================================================
# POINT D'ENTRÉE
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Programme interrompu par l'utilisateur{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.RED}✗ Erreur critique: {e}{Colors.ENDC}")
