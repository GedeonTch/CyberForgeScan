#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Informations.py - Module d'analyse et gestion de fichiers
Compatible avec CYBER FORGE SCAN
Auteur: Gedeon
"""

from __future__ import annotations
import os
import shutil
from datetime import datetime
from typing import List, Tuple

__all__ = [
    "scanner_dossier",
    "lister_gros_fichier",
    "informations",
    "organiser_fichiers",
    "all_rename",
]

# =====================================================================
# COULEURS & UI CYBER (VISIBLE)
# =====================================================================

class C:
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"

def banner():
    print(f"""
    {C.GREEN}{C.BOLD}
    ╔══════════════════════════════════════════════╗
    ║           CYBER  FORGE  SCAN                 ║
    ║          FILE ANALYSIS  MODULE               ║
    ╚══════════════════════════════════════════════╝
    {C.END}
    """)

def section(title: str):
    print(f"{C.CYAN}{'─'*55}")
    print(f"▶ {title}")
    print(f"{'─'*55}{C.END}")

# =====================================================================
# CLASSE MÉTIER
# =====================================================================

class FileAnalyzer:
    banner()
    def scan_dossier(self, chemin: str) -> None:
        section("SCAN DE DOSSIER")
        if not os.path.isdir(chemin):
            raise NotADirectoryError("Chemin invalide ou inexistant")

        fichiers = dossiers = 0
        for e in os.scandir(chemin):
            if e.is_file():
                fichiers += 1
            elif e.is_dir():
                dossiers += 1

        print(f"{C.GREEN}Chemin        :{C.END} {chemin}")
        print(f"{C.YELLOW}Sous-dossiers :{C.END} {dossiers}")
        print(f"{C.YELLOW}Fichiers      :{C.END} {fichiers}")

    def gros_fichiers(self, chemin: str, top: int = 10) -> List[Tuple[int, str]]:
        
        section("TOP FICHIERS VOLUMINEUX")

        resultats = []
        for root, _, files in os.walk(chemin):
            for f in files:
                full = os.path.join(root, f)
                try:
                    resultats.append((os.path.getsize(full), full))
                except OSError:
                    pass

        resultats.sort(reverse=True)

        for size, path in resultats[:top]:
            print(f"{C.YELLOW}{size/1024**2:8.2f} MB{C.END} | {path}")

        return resultats[:top]

    def infos_fichiers(self, chemin: str) -> None:
        
        section("INFORMATIONS FICHIERS")

        if not os.path.isdir(chemin):
            raise NotADirectoryError("Chemin invalide")

        for e in os.scandir(chemin):
            if e.is_file():
                st = e.stat()
                print(f"\n{C.GREEN}{e.name}{C.END}")
                print(f"  Taille   : {st.st_size} octets")
                print(f"  Créé     : {datetime.fromtimestamp(st.st_ctime)}")
                print(f"  Modifié  : {datetime.fromtimestamp(st.st_mtime)}")

    def organiser(self, dossier: str) -> None:
        
        section("ORGANISATION PAR EXTENSION")

        for e in os.scandir(dossier):
            if e.is_file():
                ext = os.path.splitext(e.name)[1][1:] or "sans_extension"
                cible = os.path.join(dossier, ext)
                os.makedirs(cible, exist_ok=True)
                shutil.move(e.path, os.path.join(cible, e.name))
                print(f"{C.GREEN}✓{C.END} {e.name} → {ext}/")

    def rename_all(self, dossier: str, base: str) -> None:
        
        section("RENOMMAGE EN MASSE")

        files = [f for f in os.scandir(dossier) if f.is_file()]
        for i, f in enumerate(files, 1):
            ext = os.path.splitext(f.name)[1]
            new = f"{base}_{i:03d}{ext}"
            os.rename(f.path, os.path.join(dossier, new))
            print(f"{C.GREEN}✓{C.END} {f.name} → {new}")

# =====================================================================
# API PUBLIQUE (POUR main.py)
# =====================================================================

def scanner_dossier(chemin: str) -> None:
    FileAnalyzer().scan_dossier(chemin)

def lister_gros_fichier(chemin: str, top: int = 10):
    return FileAnalyzer().gros_fichiers(chemin, top)

def informations(chemin: str) -> None:
    FileAnalyzer().infos_fichiers(chemin)

def organiser_fichiers(chemin: str) -> None:
    FileAnalyzer().organiser(chemin)

def all_rename(chemin: str, nom_base: str) -> None:
    FileAnalyzer().rename_all(chemin, nom_base)
