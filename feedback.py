#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de Feedback - CYBER FORGE SCAN
Collecte les avis et suggestions des utilisateurs
"""

import os
from datetime import datetime

# ============================================================================
# COULEURS
# ============================================================================

class Colors:
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    CYAN   = '\033[96m'
    RED    = '\033[91m'
    BOLD   = '\033[1m'
    ENDC   = '\033[0m'

# ============================================================================
# SAUVEGARDE LOCALE
# ============================================================================

FICHIER_FEEDBACK = "feedbacks.txt"

def sauvegarder_feedback(note: int, categorie: str, commentaire: str) -> bool:
    """
    Sauvegarde le feedback dans un fichier local
    
    Args:
        note: Note de 1 à 5
        categorie: Type de retour
        commentaire: Texte libre de l'utilisateur
    
    Returns:
        True si sauvegardé avec succès
    """
    try:
        with open(FICHIER_FEEDBACK, "a", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write(f"Date       : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Note       : {'★' * note}{'☆' * (5 - note)} ({note}/5)\n")
            f.write(f"Catégorie  : {categorie}\n")
            f.write(f"Commentaire: {commentaire if commentaire else '(aucun)'}\n")
            f.write("=" * 60 + "\n\n")
        return True
    except Exception as e:
        print(f"{Colors.RED}✗ Erreur lors de la sauvegarde: {e}{Colors.ENDC}")
        return False

# ============================================================================
# AFFICHAGE DES CONTACTS
# ============================================================================

def afficher_contacts():
    """Affiche les informations de contact"""
    print(f"\n{Colors.CYAN}{'─' * 50}{Colors.ENDC}")
    print(f"{Colors.BOLD}  📞  Téléphone / WhatsApp :{Colors.ENDC}  +257 66504165")
    print(f"{Colors.BOLD}  ✉️   Email               :{Colors.ENDC}  tchibanvunyagedeon@gmail.com")
    print(f"{Colors.BOLD}  🐙  GitHub               :{Colors.ENDC}  github.com/GedeonTch")
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}")
    print(f"\n  {Colors.YELLOW}⏱️  Délai de réponse : 24 à 48 heures ouvrables{Colors.ENDC}")

# ============================================================================
# COLLECTE DU FEEDBACK
# ============================================================================

def collecter_feedback():
    """
    Interface de collecte de feedback utilisateur.
    Demande une note, une catégorie et un commentaire libre.
    """
    print(f"\n{Colors.GREEN}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║         CYBER FORGE SCAN - Votre Avis Compte !           ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")

    # --- Question initiale ---
    print(f"{Colors.YELLOW}Souhaitez-vous laisser un avis sur CYBER FORGE SCAN ? (oui/non){Colors.ENDC}")
    reponse = input(f"  > ").strip().lower()

    if reponse not in ['oui', 'o', 'yes', 'y']:
        print(f"\n{Colors.CYAN}Pas de souci ! Merci d'utiliser CYBER FORGE SCAN.{Colors.ENDC}")
        print(f"{Colors.YELLOW}N'hésitez pas à revenir si vous avez des retours.{Colors.ENDC}\n")
        return

    # --- Note ---
    print(f"\n{Colors.BOLD}⭐  Donnez une note à l'outil (1 = mauvais, 5 = excellent):{Colors.ENDC}")
    note = 0
    while note not in range(1, 6):
        try:
            note = int(input(f"  Votre note [1-5] : ").strip())
            if note not in range(1, 6):
                print(f"{Colors.RED}  ✗ Entrez un chiffre entre 1 et 5.{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.RED}  ✗ Entrez un chiffre valide.{Colors.ENDC}")

    etoiles = f"{Colors.YELLOW}{'★' * note}{'☆' * (5 - note)}{Colors.ENDC}"
    print(f"  Note enregistrée : {etoiles}")

    # --- Catégorie ---
    print(f"\n{Colors.BOLD}📋  Quel type de retour souhaitez-vous laisser ?{Colors.ENDC}")
    categories = [
        "Suggestion d'amélioration",
        "Signalement d'un bug ou problème",
        "Témoignage / expérience positive",
        "Demande de nouvelle fonctionnalité",
        "Autre"
    ]
    for i, cat in enumerate(categories, 1):
        print(f"  {Colors.GREEN}[{i}]{Colors.ENDC} {cat}")

    choix_cat = 0
    while choix_cat not in range(1, len(categories) + 1):
        try:
            choix_cat = int(input(f"\n  Votre choix [1-{len(categories)}] : ").strip())
            if choix_cat not in range(1, len(categories) + 1):
                print(f"{Colors.RED}  ✗ Choix invalide.{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.RED}  ✗ Entrez un chiffre valide.{Colors.ENDC}")

    categorie = categories[choix_cat - 1]
    print(f"  Catégorie : {Colors.CYAN}{categorie}{Colors.ENDC}")

    # --- Commentaire libre ---
    print(f"\n{Colors.BOLD}💬  Votre commentaire (appuyez sur Entrée pour ignorer) :{Colors.ENDC}")
    commentaire = input(f"  > ").strip()

    # --- Résumé avant confirmation ---
    print(f"\n{Colors.CYAN}{'─' * 50}")
    print(f"  Récapitulatif de votre avis :")
    print(f"  Note       : {'★' * note}{'☆' * (5 - note)} ({note}/5)")
    print(f"  Catégorie  : {categorie}")
    print(f"  Commentaire: {commentaire if commentaire else '(aucun)'}")
    print(f"{'─' * 50}{Colors.ENDC}")

    confirmer = input(f"\n{Colors.YELLOW}Confirmer l'envoi ? (oui/non) : {Colors.ENDC}").strip().lower()

    if confirmer not in ['oui', 'o', 'yes', 'y']:
        print(f"\n{Colors.YELLOW}⚠  Avis annulé.{Colors.ENDC}\n")
        return

    # --- Sauvegarde ---
    if sauvegarder_feedback(note, categorie, commentaire):
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅  Merci pour votre retour ! Il a été enregistré.{Colors.ENDC}")
    
    # --- Affichage des contacts ---
    print(f"\n{Colors.BOLD}📬  Vous pouvez aussi nous contacter directement :{Colors.ENDC}")
    afficher_contacts()

    print(f"\n{Colors.GREEN}{'★' * 50}{Colors.ENDC}")
    print(f"{Colors.BOLD}  Types de retours bienvenus :{Colors.ENDC}")
    print(f"  {Colors.GREEN}✓{Colors.ENDC} Suggestions d'amélioration")
    print(f"  {Colors.GREEN}✓{Colors.ENDC} Signalement de problèmes")
    print(f"  {Colors.GREEN}✓{Colors.ENDC} Témoignages d'expérience")
    print(f"  {Colors.GREEN}✓{Colors.ENDC} Demandes de fonctionnalités")
    print(f"{Colors.GREEN}{'★' * 50}{Colors.ENDC}\n")


# ============================================================================
# POINT D'ENTRÉE (mode standalone)
# ============================================================================

if __name__ == "__main__":
    collecter_feedback()
