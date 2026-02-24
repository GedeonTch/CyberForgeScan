"""
Module de téléchargement YouTube pour CYBER FORGE SCAN
Utilise yt-dlp pour télécharger des vidéos/audios YouTube
Installe automatiquement les dépendances si nécessaire
"""

import os
import sys
import subprocess
from pathlib import Path
import json

def check_and_install_dependencies():
    """Vérifie et installe yt-dlp si nécessaire"""
    try:
        import yt_dlp
        print("✅ yt-dlp est déjà installé")
        return True
    except ImportError:
        print("⚠️  yt-dlp n'est pas installé")
        print("\n📦 Installation en cours (cela peut prendre 10-30 secondes)...")
        print("⏳ Merci de patienter...\n")
        
        try:
            subprocess.check_call([
                sys.executable, 
                "-m", 
                "pip", 
                "install", 
                "yt-dlp"
            ])
            print("\n✅ yt-dlp installé avec succès!")
            print("🎉 Le module est maintenant prêt à l'emploi!\n")
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Erreur lors de l'installation: {e}")
            print("\n💡 Essaye manuellement dans un terminal:")
            print("   py -m pip install yt-dlp")
            return False

# Vérifie les dépendances au chargement du module
print("🔍 Vérification des dépendances...")
if not check_and_install_dependencies():
    print("\n⚠️  Le module ne peut pas fonctionner sans yt-dlp")
    input("\nAppuie sur Entrée pour quitter...")
    sys.exit(1)

# Import après vérification
import yt_dlp


class YouTubeDownloader:
    """Gestionnaire de téléchargement YouTube avec yt-dlp"""
    
    def __init__(self, output_dir: str = "downloads"):
        """
        Initialise le downloader
        
        Args:
            output_dir: Dossier de destination des téléchargements
        """
        self.output_dir = output_dir
        Path(output_dir).mkdir(exist_ok=True)
    
    def _progress_hook(self, d):
        """Hook pour afficher la progression du téléchargement"""
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            
            if total > 0:
                percent = (downloaded / total) * 100
                print(f"\r📥 Progression: {percent:.1f}% ({downloaded/(1024*1024):.1f}/{total/(1024*1024):.1f} MB)", end='', flush=True)
        
        elif d['status'] == 'finished':
            print("\n✅ Téléchargement terminé!")
    
    def download_video(self, url: str, resolution: str = "best") -> bool:
        """
        Télécharge une vidéo YouTube
        
        Args:
            url: URL de la vidéo YouTube
            resolution: "best", "720p", "480p", "360p", etc.
        
        Returns:
            True si succès, False sinon
        """
        try:
            print(f"\n📥 Téléchargement de la vidéo...")
            
            # Configuration yt-dlp SANS fusion (pas besoin de ffmpeg)
            ydl_opts = {
                'format': 'best[height<=720]' if resolution == "best" else f'best[height<={resolution[:-1]}]',
                'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
                'quiet': True,
                'no_warnings': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Récupère les infos
                info = ydl.extract_info(url, download=False)
                print(f"📹 Titre: {info['title']}")
                print(f"👤 Auteur: {info['uploader']}")
                print(f"⏱️  Durée: {info['duration'] // 60}m {info['duration'] % 60}s")
                
                # Télécharge
                ydl.download([url])
                print(f"\n✅ Vidéo téléchargée dans '{self.output_dir}/'")
                return True
            
        except Exception as e:
            print(f"\n❌ Erreur: {str(e)}")
            return False
    
    def download_audio(self, url: str) -> bool:
        """
        Télécharge uniquement l'audio
        
        Args:
            url: URL de la vidéo YouTube
        
        Returns:
            True si succès, False sinon
        """
        try:
            print(f"\n🎵 Téléchargement de l'audio...")
            
            # Configuration pour audio uniquement
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
                'quiet': True,
                'no_warnings': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Récupère les infos
                info = ydl.extract_info(url, download=False)
                print(f"📹 Titre: {info['title']}")
                print(f"👤 Auteur: {info['uploader']}")
                
                # Télécharge
                ydl.download([url])
                print(f"\n✅ Audio téléchargé dans '{self.output_dir}/'")
                return True
            
        except Exception as e:
            print(f"\n❌ Erreur: {str(e)}")
            return False
    
    def get_video_info(self, url: str) -> dict:
        """
        Récupère les informations d'une vidéo sans télécharger
        
        Args:
            url: URL de la vidéo YouTube
        
        Returns:
            Dictionnaire avec les infos de la vidéo
        """
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Extrait les formats disponibles
                formats = []
                for f in info.get('formats', []):
                    if f.get('height'):
                        formats.append(f"{f['height']}p")
                
                return {
                    "titre": info['title'],
                    "auteur": info['uploader'],
                    "durée": f"{info['duration'] // 60}m {info['duration'] % 60}s",
                    "vues": info.get('view_count', 'N/A'),
                    "description": info['description'][:200] + "..." if len(info.get('description', '')) > 200 else info.get('description', ''),
                    "qualités_disponibles": sorted(list(set(formats)), key=lambda x: int(x[:-1]), reverse=True)
                }
            
        except Exception as e:
            return {"erreur": str(e)}
    
    def list_formats(self, url: str):
        """
        Liste tous les formats disponibles pour une vidéo
        
        Args:
            url: URL de la vidéo YouTube
        """
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                print(f"\n📹 Formats disponibles pour: {info['title']}\n")
                print("=" * 90)
                print(f"{'Format ID':<12} {'Type':<10} {'Résolution':<12} {'FPS':<6} {'Codec':<15} {'Taille':<10}")
                print("=" * 90)
                
                for f in info['formats']:
                    format_id = f.get('format_id', 'N/A')
                    ext = f.get('ext', 'N/A')
                    resolution = f"{f['height']}p" if f.get('height') else 'audio'
                    fps = f"{f.get('fps', 'N/A')}fps" if f.get('fps') else 'N/A'
                    vcodec = f.get('vcodec', 'N/A')[:15]
                    filesize = f"{f.get('filesize', 0) / (1024*1024):.1f}MB" if f.get('filesize') else 'N/A'
                    
                    print(f"{format_id:<12} {ext:<10} {resolution:<12} {fps:<6} {vcodec:<15} {filesize:<10}")
            
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")


# ============ EXEMPLE D'UTILISATION ============

def demo_downloader():
    """Fonction de démonstration du downloader"""
    print("\n🎬 CYBER FORGE SCAN - YouTube Downloader (yt-dlp)")
    print("=" * 50)
    
    downloader = YouTubeDownloader(output_dir="downloads")
    
    while True:
        print("\n📋 Options:")
        print("1. Télécharger une vidéo (meilleure qualité)")
        print("2. Télécharger l'audio uniquement")
        print("3. Voir les infos d'une vidéo")
        print("4. Lister tous les formats disponibles")
        print("5. Réinstaller/Mettre à jour yt-dlp")
        print("6. Quitter")
        
        choix = input("\nTon choix: ").strip()
        
        if choix == "6":
            print("\n👋 À bientôt!")
            break
        
        if choix == "5":
            print("\n🔄 Réinstallation de yt-dlp...")
            print("⏳ Cela peut prendre 10-30 secondes...\n")
            try:
                subprocess.check_call([
                    sys.executable, 
                    "-m", 
                    "pip", 
                    "install", 
                    "yt-dlp",
                    "--upgrade",
                    "--force-reinstall"
                ])
                print("\n✅ Réinstallation réussie!")
            except subprocess.CalledProcessError as e:
                print(f"\n❌ Erreur: {e}")
            continue
        
        if choix not in ["1", "2", "3", "4"]:
            print("❌ Choix invalide")
            continue
        
        url = input("\n🔗 URL YouTube: ").strip()
        
        if not url:
            print("❌ URL vide")
            continue
        
        if choix == "1":
            downloader.download_video(url)
        elif choix == "2":
            downloader.download_audio(url)
        elif choix == "3":
            info = downloader.get_video_info(url)
            print("\n📊 Informations de la vidéo:")
            print("=" * 50)
            for key, value in info.items():
                print(f"{key.capitalize()}: {value}")
        elif choix == "4":
            downloader.list_formats(url)
