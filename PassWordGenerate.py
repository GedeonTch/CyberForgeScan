"""
Module de Génération de Mots de Passe - CYBER FORGE SCAN
Génère des mots de passe sécurisés et teste leur robustesse
"""

import random
import string
import secrets
import hashlib
from typing import List, Dict


class PasswordGenerator:
    """Générateur et testeur de mots de passe sécurisés"""
    
    def __init__(self):
        self.maj = string.ascii_uppercase
        self.min = string.ascii_lowercase
        self.chiffres = string.digits
        self.special = string.punctuation
        self.mots_faibles = [
            "password", "admin", "azerty", "qwerty", "123456", 
            "12345678", "password123", "admin123", "welcome"
        ]
    
    def generer_avec_base(self, base: str, longueur_extra: int = 10, nombre: int = 5) -> List[str]:
        """
        Génère des mots de passe en utilisant une base fournie par l'utilisateur
        
        Args:
            base: Chaîne de base (ex: nom, date de naissance)
            longueur_extra: Nombre de caractères à ajouter
            nombre: Nombre de mots de passe à générer
        
        Returns:
            Liste de mots de passe générés
        """
        passwords = []
        caracteres = self.maj + self.min + self.chiffres + self.special
        
        for i in range(nombre):
            # Générer une partie aléatoire sécurisée
            partie_random = ''.join(secrets.choice(caracteres) for _ in range(longueur_extra))
            
            # Combiner avec la base
            password = base + partie_random
            passwords.append(password)
        
        return passwords
    
    def generer_fort(self, longueur: int = 16, nombre: int = 5) -> List[str]:
        """
        Génère des mots de passe forts sans base utilisateur
        
        Args:
            longueur: Longueur du mot de passe
            nombre: Nombre de mots de passe à générer
        
        Returns:
            Liste de mots de passe forts
        """
        if longueur < 8:
            raise ValueError("La longueur minimale est de 8 caractères")
        
        passwords = []
        
        for _ in range(nombre):
            # Garantir au moins un caractère de chaque type
            garantis = [
                secrets.choice(self.maj),
                secrets.choice(self.min),
                secrets.choice(self.chiffres),
                secrets.choice(self.special)
            ]
            
            # Compléter avec des caractères aléatoires
            caracteres_total = self.maj + self.min + self.chiffres + self.special
            reste = [secrets.choice(caracteres_total) for _ in range(longueur - 4)]
            
            # Mélanger tous les caractères
            password = garantis + reste
            secrets.SystemRandom().shuffle(password)
            
            passwords.append(''.join(password))
        
        return passwords
    
    def generer_memorable(self, nombre: int = 3) -> List[str]:
        """
        Génère des mots de passe mémorables (format: Mot-Mot-Nombre-Symbole)
        
        Args:
            nombre: Nombre de mots de passe à générer
        
        Returns:
            Liste de mots de passe mémorables
        """
        mots = [
            "Cyber","Dragon", "Soleil", "Ocean", "Montagne", "Foret", "Riviere",
            "Aigle", "Lion", "Tigre", "Phoenix", "Lune", "Etoile",
            "Tempete", "Volcan", "Cristal", "Ombre", "Lumiere", "Force"
        ]
        
        passwords = []
        
        for _ in range(nombre):
            mot1 = secrets.choice(mots)
            mot2 = secrets.choice(mots)
            nombre_random = secrets.randbelow(9000) + 1000  # 1000-9999
            symbole = secrets.choice(self.special)
            
            password = f"{mot1}{symbole}{mot2}{symbole}{nombre_random}"
            passwords.append(password)
        
        return passwords
    
    def tester_force(self, password: str) -> Dict:
        """
        Teste la force d'un mot de passe
        
        Args:
            password: Mot de passe à tester
        
        Returns:
            Dictionnaire avec les résultats du test
        """
        score = 0
        details = []
        
        # Vérifier la longueur
        if len(password) >= 12:
            score += 2
            details.append("✅ Longueur suffisante (12+ caractères)")
        elif len(password) >= 8:
            score += 1
            details.append("⚠️  Longueur acceptable (8+ caractères)")
        else:
            details.append("❌ Longueur insuffisante (< 8 caractères)")
        
        # Vérifier les majuscules
        if any(c.isupper() for c in password):
            score += 1
            details.append("✅ Contient des majuscules")
        else:
            details.append("❌ Pas de majuscules")
        
        # Vérifier les minuscules
        if any(c.islower() for c in password):
            score += 1
            details.append("✅ Contient des minuscules")
        else:
            details.append("❌ Pas de minuscules")
        
        # Vérifier les chiffres
        if any(c.isdigit() for c in password):
            score += 1
            details.append("✅ Contient des chiffres")
        else:
            details.append("❌ Pas de chiffres")
        
        # Vérifier les caractères spéciaux
        if any(c in self.special for c in password):
            score += 1
            details.append("✅ Contient des caractères spéciaux")
        else:
            details.append("❌ Pas de caractères spéciaux")
        
        # Vérifier les séquences communes
        if any(seq in password.lower() for seq in ["123", "abc", "qwerty", "azerty"]):
            score -= 1
            details.append("⚠️  Contient des séquences communes")
        
        # Vérifier les mots faibles
        if any(mot in password.lower() for mot in self.mots_faibles):
            score -= 2
            details.append("❌ Contient un mot faible (admin, password, etc.)")
        
        # Déterminer le niveau
        if score >= 5:
            niveau = "FORT 💪"
            couleur = "vert"
        elif score >= 3:
            niveau = "MOYEN ⚠️"
            couleur = "orange"
        else:
            niveau = "FAIBLE ❌"
            couleur = "rouge"
        
        # Calculer l'entropie (estimation du temps de crack)
        entropie = self._calculer_entropie(password)
        
        return {
            "score": score,
            "niveau": niveau,
            "couleur": couleur,
            "details": details,
            "entropie": entropie
        }
    
    def _calculer_entropie(self, password: str) -> Dict:
        """
        Calcule l'entropie et estime le temps de craquage
        
        Args:
            password: Mot de passe à analyser
        
        Returns:
            Dictionnaire avec les estimations
        """
        # Calculer la taille de l'espace de recherche
        espace = 0
        if any(c.islower() for c in password):
            espace += 26
        if any(c.isupper() for c in password):
            espace += 26
        if any(c.isdigit() for c in password):
            espace += 10
        if any(c in self.special for c in password):
            espace += len(self.special)
        
        # Calculer les combinaisons possibles
        import math
        combinaisons = espace ** len(password)
        bits_entropie = math.log2(combinaisons) if combinaisons > 0 else 0
        
        # Estimer le temps (en supposant 1 milliard de tentatives/seconde)
        tentatives_par_sec = 1_000_000_000
        secondes = combinaisons / tentatives_par_sec / 2  # Moyenne: moitié de l'espace
        
        # Convertir en unités lisibles
        if secondes < 60:
            temps_estime = f"{secondes:.2f} secondes"
        elif secondes < 3600:
            temps_estime = f"{secondes/60:.2f} minutes"
        elif secondes < 86400:
            temps_estime = f"{secondes/3600:.2f} heures"
        elif secondes < 31536000:
            temps_estime = f"{secondes/86400:.2f} jours"
        else:
            temps_estime = f"{secondes/31536000:.2e} années"
        
        return {
            "bits": round(bits_entropie, 2),
            "combinaisons": f"{combinaisons:.2e}",
            "temps_crack": temps_estime
        }
    
    def sauvegarder_passwords(self, passwords: List[str], fichier: str = "mots_de_passe_generes.txt"):
        """
        Sauvegarde les mots de passe dans un fichier
        
        Args:
            passwords: Liste de mots de passe
            fichier: Nom du fichier de sortie
        """
        try:
            with open(fichier, "a", encoding="utf-8") as f:
                f.write("\n" + "=" * 70 + "\n")
                f.write(f"Génération: {secrets.token_hex(4)}\n")
                f.write("=" * 70 + "\n")
                
                for i, pwd in enumerate(passwords, 1):
                    # Calculer un hash SHA-256 pour vérification
                    hash_pwd = hashlib.sha256(pwd.encode()).hexdigest()[:16]
                    f.write(f"{i}. {pwd}  (hash: {hash_pwd})\n")
                
                f.write("\n")
            
            print(f"\n✅ {len(passwords)} mots de passe sauvegardés dans '{fichier}'")
        
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")


def main():
    """Fonction principale"""
    print("\n🔐 CYBER FORGE SCAN - Générateur de Mots de Passe")
    print("=" * 60)
    
    generator = PasswordGenerator()
    
    while True:
        print("\n📋 Options:")
        print("1. Générer des mots de passe forts (sans base)")
        print("2. Générer avec une base personnalisée")
        print("3. Générer des mots de passe mémorables")
        print("4. Tester la force d'un mot de passe")
        print("5. Quitter")
        
        choix = input("\nVotre choix: ").strip()
        
        if choix == "5":
            print("\n👋 Au revoir!")
            break
        
        elif choix == "1":
            try:
                longueur = int(input("Longueur du mot de passe (8-64): ").strip() or "16")
                nombre = int(input("Nombre de mots de passe (1-10): ").strip() or "5")
                
                passwords = generator.generer_fort(longueur, min(nombre, 10))
                
                print("\n🔑 Mots de passe générés:")
                print("-" * 60)
                for i, pwd in enumerate(passwords, 1):
                    print(f"{i}. {pwd}")
                
                sauv = input("\nSauvegarder dans un fichier? (o/n): ").strip().lower()
                if sauv in ['o', 'oui', 'y']:
                    generator.sauvegarder_passwords(passwords)
            
            except ValueError as e:
                print(f"❌ Erreur: {e}")
        
        elif choix == "2":
            base = input("Entrez votre base (ex: nom, pseudo): ").strip()
            if len(base) < 3:
                print("❌ La base doit contenir au moins 3 caractères")
                continue
            
            try:
                longueur = int(input("Caractères à ajouter (4-20): ").strip() or "10")
                nombre = int(input("Nombre de variations (1-10): ").strip() or "5")
                
                passwords = generator.generer_avec_base(base, longueur, min(nombre, 10))
                
                print("\n🔑 Mots de passe générés:")
                print("-" * 60)
                for i, pwd in enumerate(passwords, 1):
                    print(f"{i}. {pwd}")
                
                sauv = input("\nSauvegarder dans un fichier? (o/n): ").strip().lower()
                if sauv in ['o', 'oui', 'y']:
                    generator.sauvegarder_passwords(passwords)
            
            except ValueError as e:
                print(f"❌ Erreur: {e}")
        
        elif choix == "3":
            try:
                nombre = int(input("Nombre de mots de passe (1-5): ").strip() or "3")
                passwords = generator.generer_memorable(min(nombre, 5))
                
                print("\n🔑 Mots de passe mémorables:")
                print("-" * 60)
                for i, pwd in enumerate(passwords, 1):
                    print(f"{i}. {pwd}")
                
                sauv = input("\nSauvegarder dans un fichier? (o/n): ").strip().lower()
                if sauv in ['o', 'oui', 'y']:
                    generator.sauvegarder_passwords(passwords)
            
            except ValueError as e:
                print(f"❌ Erreur: {e}")
        
        elif choix == "4":
            password = input("\nEntrez le mot de passe à tester: ").strip()
            
            if not password:
                print("❌ Mot de passe vide")
                continue
            
            resultat = generator.tester_force(password)
            
            print("\n" + "=" * 60)
            print(f"🔍 Analyse de: {password}")
            print("=" * 60)
            print(f"Niveau: {resultat['niveau']}")
            print(f"Score: {resultat['score']}/6")
            print(f"\n📊 Entropie: {resultat['entropie']['bits']} bits")
            print(f"🔢 Combinaisons possibles: {resultat['entropie']['combinaisons']}")
            print(f"⏱️  Temps estimé de craquage: {resultat['entropie']['temps_crack']}")
            print("\n📋 Détails:")
            for detail in resultat['details']:
                print(f"  {detail}")
        
        else:
            print("❌ Choix invalide")


if __name__ == "__main__":
    main()
# ============================================================================
# FONCTIONS WRAPPER POUR COMPATIBILITÉ AVEC MAIN.PY
# ============================================================================

def generatePswdWithInfo(base: str, longueur_extra: int = 10, nombre: int = 5):
    """
    Fonction wrapper pour main.py - Génère des mots de passe avec une base
    
    Args:
        base: Chaîne de base (ex: nom, date de naissance)
        longueur_extra: Nombre de caractères à ajouter (défaut: 10)
        nombre: Nombre de mots de passe à générer (défaut: 5)
    
    Returns:
        Liste de mots de passe générés
    """
    generator = PasswordGenerator()
    passwords = generator.generer_avec_base(base, longueur_extra, nombre)
    
    print("\n🔑 Mots de passe générés:")
    print("-" * 60)
    for i, pwd in enumerate(passwords, 1):
        print(f"{i}. {pwd}")
    
    # Sauvegarde automatique
    generator.sauvegarder_passwords(passwords, "mot de passe.txt")
    return passwords


def passWordTest(password: str):
    """
    Fonction wrapper pour main.py - Teste la force d'un mot de passe
    
    Args:
        password: Mot de passe à tester
    
    Returns:
        Dictionnaire avec les résultats du test
    """
    generator = PasswordGenerator()
    resultat = generator.tester_force(password)
    
    print("\n" + "=" * 60)
    print(f"🔍 Analyse de: {password}")
    print("=" * 60)
    print(f"Niveau: {resultat['niveau']}")
    print(f"Score: {resultat['score']}/6")
    print(f"\n📊 Entropie: {resultat['entropie']['bits']} bits")
    print(f"🔢 Combinaisons possibles: {resultat['entropie']['combinaisons']}")
    print(f"⏱️  Temps estimé de craquage: {resultat['entropie']['temps_crack']}")
    print("\n📋 Détails:")
    for detail in resultat['details']:
        print(f"  {detail}")
    
    return resultat


def genateStrong_WithoutInfo(longueur: int = 16):
    """
    Fonction wrapper pour main.py - Génère un mot de passe fort sans base
    
    Args:
        longueur: Longueur du mot de passe (défaut: 16)
    
    Returns:
        Mot de passe généré
    """
    generator = PasswordGenerator()
    passwords = generator.generer_fort(longueur, nombre=1)
    return passwords[0] if passwords else None