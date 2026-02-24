"""
Module d'enregistrement d'écran pour CYBER FORGE SCAN
Permet d'enregistrer l'écran avec audio (optionnel)
"""

import os
import sys
import subprocess
import time
from datetime import datetime
from threading import Thread

def check_and_install_dependencies():
    """Vérifie et installe les dépendances nécessaires"""
    dependencies = {
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'pyautogui': 'pyautogui',
        'PIL': 'Pillow'
    }
    
    all_installed = True
    
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {package} est déjà installé")
        except ImportError:
            print(f"⚠️  {package} n'est pas installé")
            print(f"\n📦 Installation de {package} en cours...")
            print("⏳ Merci de patienter...\n")
            
            try:
                subprocess.check_call([
                    sys.executable, 
                    "-m", 
                    "pip", 
                    "install", 
                    package
                ])
                print(f"\n✅ {package} installé avec succès!")
            except subprocess.CalledProcessError as e:
                print(f"\n❌ Échec de l'installation de {package}: {e}")
                print(f"\n💡 Essaye manuellement: py -m pip install {package}")
                all_installed = False
    
    return all_installed

# Vérifier les dépendances
print("🔍 Vérification des dépendances...")
if not check_and_install_dependencies():
    print("\n⚠️  Le module ne peut pas fonctionner sans les dépendances.")
    input("\nAppuie sur Entrée pour quitter...")
    sys.exit(1)

print("\n✅ Toutes les dépendances sont installées!")

import cv2
import numpy as np
import pyautogui
from PIL import Image


class ScreenRecorder:
    """Gestionnaire d'enregistrement d'écran"""
    
    def __init__(self, output_dir="recordings", fps=20, quality="medium"):
        """
        Initialise l'enregistreur d'écran
        
        Args:
            output_dir: Dossier de sortie pour les enregistrements
            fps: Images par seconde (10-30 recommandé)
            quality: Qualité de l'enregistrement ("low", "medium", "high")
        """
        self.output_dir = output_dir
        self.fps = fps
        self.quality = quality
        self.is_recording = False
        self.video_writer = None
        self.recording_thread = None
        
        # Créer le dossier de sortie
        os.makedirs(output_dir, exist_ok=True)
        
        # Résolution de l'écran
        self.screen_size = pyautogui.size()
        
        # Codec et qualité
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.quality_settings = {
            "low": 50,
            "medium": 75,
            "high": 95
        }
    
    def start_recording(self, filename=None, region=None):
        """
        Démarre l'enregistrement
        
        Args:
            filename: Nom du fichier (auto-généré si None)
            region: Tuple (x, y, width, height) pour enregistrer une zone spécifique
        
        Returns:
            Chemin du fichier d'enregistrement
        """
        if self.is_recording:
            print("⚠️  Un enregistrement est déjà en cours")
            return None
        
        # Générer un nom de fichier si non fourni
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screen_recording_{timestamp}.avi"
        
        if not filename.endswith('.avi'):
            filename += '.avi'
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Déterminer la taille de l'enregistrement
        if region:
            x, y, width, height = region
            screen_size = (width, height)
        else:
            screen_size = self.screen_size
        
        # Créer le VideoWriter
        self.video_writer = cv2.VideoWriter(
            filepath,
            self.fourcc,
            self.fps,
            screen_size
        )
        
        if not self.video_writer.isOpened():
            print("❌ Erreur lors de l'initialisation de l'enregistreur")
            return None
        
        # Démarrer l'enregistrement dans un thread séparé
        self.is_recording = True
        self.recording_thread = Thread(target=self._record_screen, args=(region,))
        self.recording_thread.start()
        
        print(f"\n🔴 Enregistrement démarré : {filename}")
        print(f"📊 Résolution : {screen_size[0]}x{screen_size[1]}")
        print(f"🎬 FPS : {self.fps}")
        print(f"💾 Emplacement : {os.path.abspath(filepath)}")
        
        return filepath
    
    def _record_screen(self, region=None):
        """
        Boucle d'enregistrement (exécutée dans un thread)
        
        Args:
            region: Zone à enregistrer (None = écran complet)
        """
        try:
            start_time = time.time()
            frame_count = 0
            
            while self.is_recording:
                # Capturer l'écran
                if region:
                    screenshot = pyautogui.screenshot(region=region)
                else:
                    screenshot = pyautogui.screenshot()
                
                # Convertir en format OpenCV (BGR)
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Écrire la frame
                self.video_writer.write(frame)
                frame_count += 1
                
                # Attendre pour respecter le FPS
                time.sleep(1 / self.fps)
            
            # Statistiques
            duration = time.time() - start_time
            print(f"\n📊 Statistiques de l'enregistrement :")
            print(f"   ⏱️  Durée : {duration:.1f} secondes")
            print(f"   🎞️  Frames : {frame_count}")
            print(f"   📈 FPS moyen : {frame_count / duration:.1f}")
        
        except Exception as e:
            print(f"\n❌ Erreur pendant l'enregistrement : {e}")
        
        finally:
            self._cleanup()
    
    def stop_recording(self):
        """Arrête l'enregistrement en cours"""
        if not self.is_recording:
            print("⚠️  Aucun enregistrement en cours")
            return
        
        print("\n⏹️  Arrêt de l'enregistrement...")
        self.is_recording = False
        
        # Attendre la fin du thread
        if self.recording_thread:
            self.recording_thread.join()
        
        print("✅ Enregistrement terminé")
    
    def _cleanup(self):
        """Nettoie les ressources"""
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
    
    def get_screen_info(self):
        """Affiche les informations sur l'écran"""
        print("\n🖥️  Informations de l'écran :")
        print(f"   📐 Résolution : {self.screen_size[0]}x{self.screen_size[1]}")
        print(f"   🎬 FPS configuré : {self.fps}")
        print(f"   💎 Qualité : {self.quality}")


def enregistrement_temps_limite(recorder, duree_secondes):
    """
    Enregistre pendant une durée spécifique
    
    Args:
        recorder: Instance de ScreenRecorder
        duree_secondes: Durée en secondes
    """
    filepath = recorder.start_recording()
    
    if filepath:
        print(f"\n⏱️  Enregistrement pour {duree_secondes} secondes...")
        
        # Compte à rebours
        for i in range(duree_secondes, 0, -1):
            if i <= 5:
                print(f"   {i}...", end=" ", flush=True)
            time.sleep(1)
        
        print("\n")
        recorder.stop_recording()


def enregistrement_region(recorder):
    """
    Enregistre une région spécifique de l'écran
    
    Args:
        recorder: Instance de ScreenRecorder
    """
    print("\n📐 Définition de la région à enregistrer")
    print("Déplace ta souris vers le coin supérieur gauche de la région")
    input("Appuie sur Entrée quand c'est prêt...")
    
    x1, y1 = pyautogui.position()
    print(f"✅ Coin supérieur gauche : ({x1}, {y1})")
    
    print("\nDéplace ta souris vers le coin inférieur droit de la région")
    input("Appuie sur Entrée quand c'est prêt...")
    
    x2, y2 = pyautogui.position()
    print(f"✅ Coin inférieur droit : ({x2}, {y2})")
    
    # Calculer la région
    x = min(x1, x2)
    y = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    
    region = (x, y, width, height)
    print(f"\n📊 Région : {width}x{height} pixels à partir de ({x}, {y})")
    
    duree = int(input("\nDurée de l'enregistrement (secondes) : "))
    
    filepath = recorder.start_recording(region=region)
    
    if filepath:
        print(f"\n⏱️  Enregistrement pour {duree} secondes...")
        time.sleep(duree)
        recorder.stop_recording()


# ============ PROGRAMME PRINCIPAL ============

def demo_screen_recorder():
    """Interface interactive de l'enregistreur d'écran"""
    print("\n🎬 CYBER FORGE SCAN - Enregistreur d'Écran")
    print("=" * 50)
    
    # Configuration
    print("\n⚙️  Configuration")
    fps = input("FPS (10-30, défaut 20) : ").strip() or "20"
    quality = input("Qualité (low/medium/high, défaut medium) : ").strip() or "medium"
    
    recorder = ScreenRecorder(fps=int(fps), quality=quality)
    recorder.get_screen_info()
    
    while True:
        print("\n" + "=" * 50)
        print("📋 Options :")
        print("1. Démarrer un enregistrement manuel")
        print("2. Enregistrement avec durée limitée")
        print("3. Enregistrer une région spécifique")
        print("4. Voir les informations de l'écran")
        print("5. Changer les paramètres")
        print("6. Quitter")
        
        choix = input("\nTon choix : ").strip()
        
        if choix == "6":
            # Arrêter l'enregistrement si en cours
            if recorder.is_recording:
                recorder.stop_recording()
            print("\n👋 À bientôt!")
            break
        
        elif choix == "1":
            if recorder.is_recording:
                print("\n⚠️  Un enregistrement est déjà en cours")
                arreter = input("Veux-tu l'arrêter ? (o/n) : ").strip().lower()
                if arreter in ['o', 'oui', 'y', 'yes']:
                    recorder.stop_recording()
            else:
                filename = input("\nNom du fichier (vide = auto) : ").strip() or None
                recorder.start_recording(filename)
                
                input("\n⏸️  Appuie sur Entrée pour arrêter l'enregistrement...")
                recorder.stop_recording()
        
        elif choix == "2":
            duree = input("\nDurée en secondes : ").strip()
            try:
                duree_int = int(duree)
                enregistrement_temps_limite(recorder, duree_int)
            except ValueError:
                print("❌ Durée invalide")
        
        elif choix == "3":
            enregistrement_region(recorder)
        
        elif choix == "4":
            recorder.get_screen_info()
        
        elif choix == "5":
            fps = input("\nNouveau FPS (actuel: {}): ".format(recorder.fps)).strip()
            if fps:
                recorder.fps = int(fps)
                print(f"✅ FPS changé à {recorder.fps}")
            
            quality = input("Nouvelle qualité (actuel: {}): ".format(recorder.quality)).strip()
            if quality in ["low", "medium", "high"]:
                recorder.quality = quality
                print(f"✅ Qualité changée à {recorder.quality}")
        
        else:
            print("❌ Choix invalide")


if __name__ == "__main__":
    demo_screen_recorder()