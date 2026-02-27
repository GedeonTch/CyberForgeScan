"""
Module de Démonstration Bruteforce - CYBER FORGE SCAN
Démontre la vulnérabilité des mots de passe faibles (ÉDUCATIF UNIQUEMENT)
Version éthique avec limitations et avertissements
"""
 
import time
import string
import itertools
import hashlib
from typing import Optional, Tuple


class BruteForceDemo:
    """
    Démonstrateur de force brute pour fins éducatives
    AVERTISSEMENT: Usage strictement éducatif uniquement
    """
    
    def __init__(self):
        self.chars_simple = string.ascii_lowercase + string.digits
        self.chars_medium = string.ascii_letters + string.digits
        self.chars_complex = string.printable.strip()
        
        # Limitations éthiques
        self.max_length = 4  # Maximum 4 caractères pour éviter les abus
        self.max_attempts = 10000000  # Limite de tentatives
        self.delay_between_attempts = 0.0001  # Délai minimal
        
    def afficher_avertissement(self):
        """Affiche un avertissement éthique et légal"""
        print("\n" + "=" * 70)
        print("⚠️  AVERTISSEMENT ÉTHIQUE ET LÉGAL")
        print("=" * 70)
        print("Ce module est uniquement destiné à des fins ÉDUCATIVES.")
        print("Il démontre pourquoi les mots de passe faibles sont dangereux.")
        print()
        print("❌ Il est ILLÉGAL d'utiliser cet outil pour:")
        print("   • Accéder à des comptes qui ne vous appartiennent pas")
        print("   • Tester des systèmes sans autorisation explicite")
        print("   • Toute activité malveillante ou non autorisée")
        print()
        print("✅ Utilisations légales:")
        print("   • Tester VOS PROPRES mots de passe")
        print("   • Comprendre l'importance de mots de passe forts")
        print("   • Démonstrations éducatives avec autorisation")
        print("=" * 70)
        print()
        
        reponse = input("Acceptez-vous ces conditions? (oui/non): ").strip().lower()
        if reponse not in ['oui', 'yes', 'o', 'y']:
            print("\n❌ Accès refusé. Utilisez cet outil de manière responsable.")
            return False
        return True
    
    def estimer_temps(self, password: str, charset: str = "simple") -> dict:
        """
        Estime le temps nécessaire pour craquer un mot de passe
        
        Args:
            password: Mot de passe à analyser
            charset: Type de jeu de caractères ('simple', 'medium', 'complex')
        
        Returns:
            Dictionnaire avec les estimations
        """
        # Déterminer la taille du jeu de caractères
        if charset == "simple":
            taille_charset = len(self.chars_simple)
            nom_charset = "minuscules + chiffres"
        elif charset == "medium":
            taille_charset = len(self.chars_medium)
            nom_charset = "lettres + chiffres"
        else:
            taille_charset = len(self.chars_complex)
            nom_charset = "tous caractères"
        
        longueur = len(password)
        
        # Calculer les combinaisons possibles
        combinaisons = taille_charset ** longueur
        
        # Estimer le temps (1 million de tentatives/seconde)
        tentatives_par_sec = 1_000_000
        secondes = combinaisons / tentatives_par_sec / 2  # Moyenne
        
        # Convertir en unités lisibles
        if secondes < 1:
            temps_str = f"{secondes * 1000:.2f} millisecondes"
        elif secondes < 60:
            temps_str = f"{secondes:.2f} secondes"
        elif secondes < 3600:
            temps_str = f"{secondes/60:.2f} minutes"
        elif secondes < 86400:
            temps_str = f"{secondes/3600:.2f} heures"
        elif secondes < 31536000:
            temps_str = f"{secondes/86400:.2f} jours"
        else:
            temps_str = f"{secondes/31536000:.2e} années"
        
        return {
            "longueur": longueur,
            "charset": nom_charset,
            "taille_charset": taille_charset,
            "combinaisons": combinaisons,
            "temps_moyen": temps_str,
            "secondes": secondes
        }
    
    def analyser_vulnerabilite(self, password: str) -> dict:
        """
        Analyse la vulnérabilité d'un mot de passe
        
        Args:
            password: Mot de passe à analyser
        
        Returns:
            Dictionnaire avec l'analyse de vulnérabilité
        """
        vulnerabilites = []
        points_forts = []
        score = 0
        
        # Analyser la longueur
        if len(password) < 6:
            vulnerabilites.append("❌ CRITIQUE: Longueur < 6 caractères (très facile à craquer)")
        elif len(password) < 8:
            vulnerabilites.append("⚠️  FAIBLE: Longueur < 8 caractères (vulnérable)")
            score += 1
        else:
            points_forts.append("✅ Longueur suffisante (≥ 8 caractères)")
            score += 2
        
        # Analyser le type de caractères
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        types_count = sum([has_lower, has_upper, has_digit, has_special])
        
        if types_count == 1:
            vulnerabilites.append("❌ CRITIQUE: Un seul type de caractères")
        elif types_count == 2:
            vulnerabilites.append("⚠️  FAIBLE: Seulement 2 types de caractères")
            score += 1
        else:
            points_forts.append(f"✅ Diversité: {types_count} types de caractères")
            score += 2
        
        # Vérifier les patterns communs
        patterns_faibles = [
            "123", "abc", "password", "admin", "qwerty", "azerty",
            "000", "111", "aaa", "hello", "welcome"
        ]
        
        for pattern in patterns_faibles:
            if pattern in password.lower():
                vulnerabilites.append(f"❌ CRITIQUE: Contient le pattern '{pattern}'")
                score -= 2
                break
        
        # Vérifier les répétitions
        if any(password[i] == password[i+1] == password[i+2] for i in range(len(password)-2)):
            vulnerabilites.append("⚠️  FAIBLE: Contient des répétitions (aaa, 111)")
            score -= 1
        
        # Déterminer le niveau de vulnérabilité
        if score <= 0:
            niveau = "🔴 TRÈS VULNÉRABLE"
            conseil = "Ce mot de passe peut être cracké en quelques secondes!"
        elif score <= 2:
            niveau = "🟡 VULNÉRABLE"
            conseil = "Ce mot de passe est faible. Augmentez la complexité."
        else:
            niveau = "🟢 RÉSISTANT"
            conseil = "Mot de passe acceptable, mais peut être amélioré."
        
        return {
            "niveau": niveau,
            "score": score,
            "vulnerabilites": vulnerabilites,
            "points_forts": points_forts,
            "conseil": conseil
        }
    
    def demo_bruteforce_limite(self, password: str, max_length: int = 4) -> Tuple[Optional[str], int, float]:
        """
        Démonstration limitée de bruteforce (max 4 caractères)
        
        Args:
            password: Mot de passe à trouver
            max_length: Longueur maximale à tester
        
        Returns:
            Tuple (mot_de_passe_trouvé, tentatives, temps_écoulé)
        """
        if len(password) > max_length:
            print(f"⚠️  Le mot de passe est trop long (>{max_length} caractères)")
            print(f"   Cette démonstration est limitée pour des raisons éthiques.")
            return None, 0, 0.0
        
        if len(password) > self.max_length:
            print(f"❌ Longueur maximale autorisée: {self.max_length} caractères")
            return None, 0, 0.0
        
        print(f"\n🔍 Démonstration de bruteforce (ÉDUCATIF)")
        print(f"Longueur du mot de passe: {len(password)}")
        print(f"Recherche en cours...\n")
        
        chars = self.chars_simple
        tentatives = 0
        debut = time.time()
        
        for longueur in range(1, len(password) + 1):
            for guess in itertools.product(chars, repeat=longueur):
                tentatives += 1
                guess_str = "".join(guess)
                
                # Afficher la progression tous les 1000 essais
                if tentatives % 1000 == 0:
                    print(f"Tentative {tentatives}: {guess_str}")
                
                time.sleep(self.delay_between_attempts)
                
                if guess_str == password:
                    temps_ecoule = time.time() - debut
                    print(f"\n✅ MOT DE PASSE TROUVÉ: {guess_str}")
                    print(f"⏱️  Temps écoulé: {temps_ecoule:.2f} secondes")
                    print(f"🔢 Tentatives: {tentatives}")
                    return guess_str, tentatives, temps_ecoule
                
                if tentatives >= self.max_attempts:
                    print(f"\n⚠️  Limite de tentatives atteinte ({self.max_attempts})")
                    return None, tentatives, time.time() - debut
        
        return None, tentatives, time.time() - debut
    
    def demo_interactive(self):
        """Mode interactif de démonstration"""
        if not self.afficher_avertissement():
            return
        
        print("\n🎓 MODE DÉMONSTRATION ÉDUCATIVE")
        print("=" * 70)
        print("Ce mode vous permet de comprendre pourquoi les mots de passe")
        print("courts et simples sont dangereux.\n")
        
        while True:
            print("\n📋 Options:")
            print("1. Estimer le temps de craquage")
            print("2. Analyser la vulnérabilité")
            print("3. Démonstration bruteforce (max 35 caractères)")
            print("4. Voir des exemples")
            print("5. Retour")
            
            choix = input("\nVotre choix: ").strip()
            
            if choix == "5":
                break
            
            elif choix == "1":
                password = input("\nEntrez un mot de passe à analyser: ").strip()
                if not password:
                    print("❌ Mot de passe vide")
                    continue
                
                print("\n📊 ESTIMATION DU TEMPS DE CRAQUAGE")
                print("=" * 70)
                
                for charset in ["simple", "medium", "complex"]:
                    est = self.estimer_temps(password, charset)
                    print(f"\nJeu de caractères: {est['charset']}")
                    print(f"  Taille: {est['taille_charset']} caractères")
                    print(f"  Combinaisons: {est['combinaisons']:,}")
                    print(f"  Temps moyen: {est['temps_moyen']}")
            
            elif choix == "2":
                password = input("\nEntrez un mot de passe à analyser: ").strip()
                if not password:
                    print("❌ Mot de passe vide")
                    continue
                
                analyse = self.analyser_vulnerabilite(password)
                
                print("\n🔍 ANALYSE DE VULNÉRABILITÉ")
                print("=" * 70)
                print(f"Niveau: {analyse['niveau']}")
                print(f"Score: {analyse['score']}/4")
                print(f"\n{analyse['conseil']}")
                
                if analyse['vulnerabilites']:
                    print("\n⚠️  Vulnérabilités détectées:")
                    for vuln in analyse['vulnerabilites']:
                        print(f"  {vuln}")
                
                if analyse['points_forts']:
                    print("\n✅ Points forts:")
                    for fort in analyse['points_forts']:
                        print(f"  {fort}")
            
            elif choix == "3":
                password = input("\nEntrez un mot de passe simple (max 4 caractères): ").strip()
                if not password:
                    print("❌ Mot de passe vide")
                    continue
                
                confirm = input(f"\n⚠️  Lancer la démonstration pour '{password}'? (oui/non): ").strip().lower()
                if confirm in ['oui', 'yes', 'o', 'y']:
                    self.demo_bruteforce_limite(password, max_length=4)
            
            elif choix == "4":
                print("\n📚 EXEMPLES DE VULNÉRABILITÉS")
                print("=" * 70)
                
                exemples = [
                    ("123", "❌ TRÈS FAIBLE: Cracké en millisecondes"),
                    ("pass", "❌ TRÈS FAIBLE: Cracké en secondes"),
                    ("admin123", "⚠️  FAIBLE: Cracké en minutes/heures"),
                    ("Passw0rd!", "🟡 MOYEN: Meilleur mais prévisible"),
                    ("aB3$xY9*mK2#", "✅ FORT: Très difficile à craquer"),
                ]
                
                print("\nExemples de mots de passe et leur résistance:")
                for pwd, desc in exemples:
                    print(f"\n  '{pwd}'")
                    print(f"  {desc}")
                
                print("\n💡 CONSEILS:")
                print("  • Utilisez au moins 12 caractères")
                print("  • Mélangez majuscules, minuscules, chiffres et symboles")
                print("  • Évitez les mots du dictionnaire")
                print("  • Utilisez un gestionnaire de mots de passe")
                print("  • Activez l'authentification à deux facteurs (2FA)")
            
            else:
                print("❌ Choix invalide")


# ============================================================================
# FONCTIONS POUR COMPATIBILITÉ AVEC MAIN.PY
# ============================================================================

def buteforce(password: str) -> Optional[str]:
    """
    Fonction wrapper pour compatibilité (avec limitations éthiques)
    
    Args:
        password: Mot de passe à tester
    
    Returns:
        Mot de passe si trouvé, None sinon
    """
    demo = BruteForceDemo()
    
    if not demo.afficher_avertissement():
        return None

    
    if len(password) > 4:
        print(f"\n⚠️  Ce module est limité à 4 caractères pour des raisons éthiques.")
        print(f"   Le mot de passe '{password}' est trop long pour cette démonstration.")
        print(f"\n💡 Pour tester la force de mots de passe plus longs,")
        print(f"   utilisez le module 'PassWordGenerate' → option 'Tester la force'")
        return None
    
    result, tentatives, temps = demo.demo_bruteforce_limite(password, max_length=4)
    return result


def demo_bruteforce():
    """Lance le mode démonstration interactif"""
    demo = BruteForceDemo()
    demo.demo_interactive()


def main():
    """Fonction principale - mode standalone"""
    print("\n🔐 CYBER FORGE SCAN - Démonstration Bruteforce")
    print("=" * 70)
    
    demo = BruteForceDemo()
    demo.demo_interactive()
    demo.BruteForceBasique()


if __name__ == "__main__":
    main()