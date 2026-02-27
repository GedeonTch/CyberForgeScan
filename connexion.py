"""
Module de test de vitesse Internet pour CYBER FORGE SCAN
Mesure la vitesse de téléchargement, upload et ping
"""

import time
import sys
import subprocess

def check_and_install_speedtest():
    """Vérifie et installe speedtest-cli si nécessaire"""
    try:
        import speedtest
        print("✅ speedtest-cli est déjà installé")
        return True
    except ImportError:
        print("⚠️  speedtest-cli n'est pas installé")
        print("\n📦 Installation en cours (cela peut prendre 10-30 secondes)...")
        print("⏳ Merci de patienter...\n")
        
        try:
            subprocess.check_call([
                sys.executable, 
                "-m", 
                "pip", 
                "install", 
                "speedtest-cli"
            ])
            print("\n✅ speedtest-cli installé avec succès!")
            print("🎉 Le module est maintenant prêt à l'emploi!\n")
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Erreur lors de l'installation: {e}")
            print("\n💡 Essaye manuellement dans un terminal:")
            print("   py -m pip install speedtest-cli")
            return False

# Vérifie les dépendances
print("🔍 Vérification des dépendances...")
if not check_and_install_speedtest():
    print("\n⚠️  Le module ne peut pas fonctionner sans speedtest-cli")
    input("\nAppuie sur Entrée pour quitter...")
    sys.exit(1)

import speedtest


def check_internet_speed():
    """
    Teste la vitesse de connexion Internet
    
    Returns:
        dict: Dictionnaire avec download, upload et ping
        None: En cas d'erreur
    """
    try:
        print("\n🌐 Test de vitesse Internet en cours...")
        print("⏳ Cela peut prendre 30-60 secondes...\n")
        
        st = speedtest.Speedtest()
        
        # Sélection du meilleur serveur
        print("🔍 Recherche du meilleur serveur...")
        st.get_best_server()
        
        # Test de ping
        print("📡 Test du ping...")
        ping = st.results.ping
        
        # Test de download
        print("📥 Test de téléchargement...")
        download = st.download() / 1_000_000  # Conversion en Mbps
        
        # Test d'upload
        print("📤 Test d'envoi...")
        upload = st.upload() / 1_000_000  # Conversion en Mbps
        
        return {
            "download": round(download, 2),
            "upload": round(upload, 2),
            "ping": round(ping, 2)
        }
        
    except speedtest.ConfigRetrievalError:
        print("❌ Erreur: Impossible de récupérer la configuration du test")
        print("Veuillez vérifier votre connexion")
        return None
    except speedtest.SpeedtestException as e:
        print(f"❌ Erreur lors du test: {e}")
        return None
    except Exception as exc:
        print(f"❌ Erreur inconnue: {exc}")
        return None


def display_speed_results(speed):
    """
    Affiche les résultats de manière formatée
    
    Args:
        speed: Dictionnaire avec les résultats du test
    """
    if not speed:
        print("\n❌ Test échoué")
        return
    
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS DU TEST DE VITESSE")
    print("=" * 50)
    print(f"📥 Download : {speed['download']} Mbps")
    print(f"📤 Upload   : {speed['upload']} Mbps")
    print(f"⏱️  Ping     : {speed['ping']} ms")
    print("=" * 50)
    
    # Évaluation de la connexion
    if speed['download'] > 100:
        print("🚀 Connexion excellente!")
    elif speed['download'] > 50:
        print("✅ Bonne connexion")
    elif speed['download'] > 10:
        print("⚠️  Connexion moyenne")
    else:
        print("🐌 Connexion lente")


def compare_speeds():
    """Compare plusieurs tests de vitesse"""
    results = []
    num_tests = int(input("\nCombien de tests veux-tu effectuer ? (1-5): ").strip() or "1")
    
    for i in range(min(num_tests, 5)):
        print(f"\n📊 Test {i+1}/{num_tests}")
        speed = check_internet_speed()
        if speed:
            results.append(speed)
            display_speed_results(speed)
        
        if i < num_tests - 1:
            time.sleep(2)  # Pause entre les tests
    
    # Moyenne des résultats
    if len(results) > 1:
        avg_download = sum(r['download'] for r in results) / len(results)
        avg_upload = sum(r['upload'] for r in results) / len(results)
        avg_ping = sum(r['ping'] for r in results) / len(results)
        
        print("\n" + "=" * 50)
        print("📈 MOYENNE DES TESTS")
        print("=" * 50)
        print(f"📥 Download moyen : {round(avg_download, 2)} Mbps")
        print(f"📤 Upload moyen   : {round(avg_upload, 2)} Mbps")
        print(f"⏱️  Ping moyen     : {round(avg_ping, 2)} ms")
        print("=" * 50)

 
# ============ UTILISATION ============

def demo_speedtest():
    """Fonction de démonstration du test de vitesse"""
    print("\n🌐 CYBER FORGE SCAN - Test de Vitesse Internet")
    print("=" * 50)
    
    while True:
        print("\n📋 Options:")
        print("1. Tester la vitesse Internet")
        print("2. Effectuer plusieurs tests et comparer")
        print("3. Quitter")
        
        choix = input("\nTon choix: ").strip()
        
        if choix == "3":
            print("\n👋 À bientôt!")
            break
        
        if choix == "1":
            speed = check_internet_speed()
            display_speed_results(speed)
        
        elif choix == "2":
            compare_speeds()
        
        else:
            print("❌ Choix invalide")


if __name__ == "__main__":
    demo_speedtest()