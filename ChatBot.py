"""
AI Assistant Module pour CYBER FORGE SCAN
Utilise Ollama pour fournir une assistance conversationnelle légère
"""

import requests
import json
import sys
import subprocess
from typing import Optional

def check_and_install_dependencies():
    """Vérifie et installe requests si nécessaire"""
    try:
        import requests
        print("✅ requests est déjà installé")
        return True
    except ImportError:
        print("⚠️  requests n'est pas installé")
        print("\n📦 Installation en cours...")
        print("⏳ Merci de patienter...\n")
        
        try:
            subprocess.check_call([
                sys.executable, 
                "-m", 
                "pip", 
                "install", 
                "requests"
            ])
            print("\n✅ requests installé avec succès!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Erreur lors de l'installation: {e}")
            print("\n💡 Essaye manuellement: py -m pip install requests")
            return False

# Vérifier les dépendances
print("🔍 Vérification des dépendances...")
if not check_and_install_dependencies():
    print("\n⚠️  Le module ne peut pas fonctionner sans requests")
    input("\nAppuie sur Entrée pour quitter...")
    sys.exit(1)

import requests


class CyberForgeAssistant:
    """Assistant IA local pour répondre aux questions des utilisateurs"""
    
    def __init__(self, model: str = "phi3:mini", base_url: str = "http://localhost:11434"):
        """
        Initialise l'assistant
        
        Args:
            model: Nom du modèle Ollama (phi3:mini, gpt-oss:20b-cloud, etc.)
            base_url: URL de l'API Ollama locale
        """
        self.model = model
        self.base_url = base_url
        self.conversation_history = []
        
    def check_ollama_status(self) -> bool:
        """Vérifie si Ollama est en cours d'exécution"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_available_models(self) -> list:
        """Liste les modèles Ollama disponibles"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model["name"] for model in models]
            return []
        except:
            return []
    
    def ask(self, question: str, context: Optional[str] = None, stream: bool = False) -> str:
        """
        Pose une question à l'assistant
        
        Args:
            question: Question de l'utilisateur
            context: Contexte optionnel (infos sur CYBER FORGE SCAN)
            stream: Afficher la réponse en temps réel (True/False)
        
        Returns:
            Réponse de l'assistant
        """
        # Vérifie qu'Ollama tourne
        if not self.check_ollama_status():
            return "❌ Erreur: Ollama n'est pas démarré. Lance 'ollama serve' dans un terminal."
        
        # Prépare le prompt avec contexte si fourni
        prompt = question
        if context:
            prompt = f"Contexte: {context}\n\nQuestion: {question}"
        
        # Ajoute à l'historique
        self.conversation_history.append({"role": "user", "content": prompt})
        
        try:
            # Appel API Ollama
            if stream:
                return self._ask_stream(prompt)
            else:
                return self._ask_normal()
                
        except requests.exceptions.Timeout:
            return "⏱️ Timeout: La requête a pris trop de temps. Réessaye."
        except requests.exceptions.RequestException as e:
            return f"❌ Erreur de connexion: {str(e)}"
        except Exception as e:
            return f"❌ Erreur inattendue: {str(e)}"
    
    def _ask_normal(self) -> str:
        """Requête normale sans streaming"""
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": self.conversation_history,
                "stream": False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            assistant_response = result["message"]["content"]
            
            # Ajoute la réponse à l'historique
            self.conversation_history.append({
                "role": "assistant", 
                "content": assistant_response
            })
            
            return assistant_response
        else:
            return f"❌ Erreur API Ollama: {response.status_code}"
    
    def _ask_stream(self, prompt: str) -> str:
        """Requête avec streaming (affichage en temps réel)"""
        print("\n🤖 Assistant: ", end="", flush=True)
        
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": self.conversation_history,
                "stream": True
            },
            stream=True,
            timeout=60
        )
        
        full_response = ""
        
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    if "message" in data:
                        chunk = data["message"].get("content", "")
                        print(chunk, end="", flush=True)
                        full_response += chunk
                except json.JSONDecodeError:
                    continue
        
        print()  # Nouvelle ligne après le streaming
        
        # Ajoute la réponse complète à l'historique
        self.conversation_history.append({
            "role": "assistant", 
            "content": full_response
        })
        
        return full_response
    
    def reset_conversation(self):
        """Réinitialise l'historique de conversation"""
        self.conversation_history = []
        print("🔄 Conversation réinitialisée!")
    
    def change_model(self, new_model: str):
        """Change le modèle utilisé"""
        available = self.get_available_models()
        if new_model in available:
            self.model = new_model
            print(f"✅ Modèle changé pour: {new_model}")
            self.reset_conversation()
        else:
            print(f"❌ Modèle {new_model} non disponible")
            print(f"📋 Modèles disponibles: {', '.join(available)}")


# ============ EXEMPLE D'UTILISATION ============

def demo_assistant():
    """Fonction de démonstration de l'assistant"""
    print("\n🤖 CYBER FORGE SCAN - Assistant NOVA IA")
    print("=" * 50)
    
    # Initialise l'assistant
    assistant = CyberForgeAssistant(model="phi3:mini")
    
    # Vérifie le statut
    if not assistant.check_ollama_status():
        print("\n❌ Ollama n'est pas démarré!")
        print("💡 Lance dans un terminal: ollama serve")
        input("\nAppuie sur Entrée pour quitter...")
        return
    
    # Liste les modèles disponibles
    models = assistant.get_available_models()
    print(f"\n✅ Ollama est en ligne!")
    print("\nDemmarage de NOVA!")
    print(f"📋 Modèles disponibles: {', '.join(models)}")
    print(f"🎯 Modèle actuel: {assistant.model}")
    
    print("\n💬 Commandes spéciales:")
    print("  - 'exit' ou 'quit' : Quitter NOVA")
    print("  - 'reset' : Nouvelle conversation avec NOVA")
    print("  - 'model' : Changer de modèle")
    print("  - 'stream on/off' : Activer/désactiver le streaming")
    
    # Contexte sur l'outil
    context = """
    CYBER FORGE SCAN est un outil de cybersécurité Python qui permet de:
    - Scanner les vulnérabilités
    - Télécharger des vidéos YouTube
    - Convertir des documents en PDF
    - Tester la vitesse Internet
    - Utiliser une IA locale via Ollama
    
    L'utilisateur peut avoir des questions sur l'utilisation, les résultats,
    ou des concepts de cybersécurité en général.
    """
    
    stream_mode = False
    
    print("\n" + "=" * 50)
    print("🚀 L'assistant NOVA est prêt!")
    print("=" * 50 + "\n")
    
    while True:
        user_input = input("Toi: ").strip()
        
        if not user_input:
            continue
        
        # Commandes spéciales
        if user_input.lower() in ['exit', 'quit']:
            print("\n👋 À bientôt!")
            break
        
        if user_input.lower() == 'reset':
            assistant.reset_conversation()
            continue
        
        if user_input.lower() == 'model':
            print(f"\n📋 Modèles disponibles: {', '.join(models)}")
            new_model = input("Nouveau modèle: ").strip()
            if new_model:
                assistant.change_model(new_model)
            continue
        
        if user_input.lower() == 'stream on':
            stream_mode = True
            print("✅ Streaming activé")
            continue
        
        if user_input.lower() == 'stream off':
            stream_mode = False
            print("✅ Streaming désactivé")
            continue
        
        # Question normale
        if not stream_mode:
            print("\n🤖 Assistant NOVA: ", end="", flush=True)
        
        response = assistant.ask(user_input, context=context, stream=stream_mode)
        
        if not stream_mode:
            print(response + "\n")


if __name__ == "__main__":
    demo_assistant()