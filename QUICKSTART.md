# 🚀 GUIDE DE DÉMARRAGE RAPIDE

## Installation en 3 étapes

### 1️⃣ Télécharger le projet
```bash
# Option A: Avec Git
git clone https://github.com/votre-username/cyber-forge-scan.git
cd cyber-forge-scan

# Option B: Sans Git
# Télécharger le ZIP depuis GitHub
# Extraire et ouvrir le dossier dans un terminal
```

### 2️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

**Note:** Si vous avez des erreurs, essayez :
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3️⃣ Lancer le programme
```bash
python main.py
```

---

## 🎯 Première utilisation

### Test rapide: Générer un mot de passe
1. Lancer `python main.py`
2. Choisir `[2]` (Gestion des Mots de Passe)
3. Choisir `[3]` (Générer un mot de passe aléatoire)
4. Entrer `20` pour la longueur
5. ✅ Vous obtenez un mot de passe ultra-sécurisé !

### Test complet: Analyser un fichier
1. Créer un fichier test `test.log` avec ce contenu:
```
2024-02-07 admin@example.com accessed from 192.168.1.1
ERROR: Permission denied for user@test.com
10:30AM - Connection from 10.0.0.5
```

2. Lancer `python main.py`
3. Choisir `[1]` (Analyse & Extraction)
4. Choisir `[1]` (Analyser un fichier log)
5. Entrer le chemin de `test.log`
6. ✅ Le programme extrait emails, IPs, dates et alerte sur "ERROR"

---

## 📋 Commandes essentielles

### Installation complète
```bash
# Cloner
git clone https://github.com/votre-username/cyber-forge-scan.git
cd cyber-forge-scan

# Installer
pip install -r requirements.txt

# Tester
python main.py
```

### Avec Ollama (Assistant IA)
```bash
# 1. Installer Ollama
# Télécharger depuis https://ollama.ai

# 2. Télécharger un modèle
ollama pull phi3:mini

# 3. Lancer le serveur Ollama
ollama serve

# 4. Dans un autre terminal, lancer CYBER FORGE SCAN
python main.py
# Choisir [6] Assistant IA
```

### Mise à jour
```bash
# Avec Git
git pull origin main
pip install -r requirements.txt --upgrade

# Sans Git
# Re-télécharger le ZIP et remplacer les fichiers
pip install -r requirements.txt --upgrade
```

---

## ❓ Questions Fréquentes

### Q: J'ai une erreur "Module not found"
**R:** Installez les dépendances:
```bash
pip install -r requirements.txt
```

### Q: Les couleurs ne s'affichent pas sur Windows
**R:** Utilisez Windows Terminal ou installez `colorama`:
```bash
pip install colorama
```

### Q: Comment quitter le programme?
**R:** Tapez `0` dans le menu principal, ou `Ctrl+C`

### Q: Ollama ne fonctionne pas
**R:** Vérifiez que:
1. Ollama est installé: `ollama --version`
2. Un modèle est téléchargé: `ollama list`
3. Le serveur tourne: `ollama serve`

### Q: Puis-je utiliser cet outil professionnellement?
**R:** Non, usage éducatif uniquement. Pour un usage commercial, contactez l'auteur.

---

## 🆘 Besoin d'aide?

1. 📖 Lisez le [README.md](README.md) complet
2. 🔍 Vérifiez les [Issues GitHub](https://github.com/votre-username/cyber-forge-scan/issues)
3. 💬 Ouvrez une nouvelle Issue

---

## 🎓 Tutoriels recommandés

### 1. Générer et tester des mots de passe
```bash
python main.py
[2] → [1] → Entrer "MonMotDePasse" → Entrer "10"
```

### 2. Analyser des logs système
```bash
python main.py
[1] → [1] → Entrer "/var/log/syslog"
```

### 3. Télécharger une vidéo YouTube
```bash
python main.py
[5] → [1] → Coller l'URL YouTube
```

### 4. Tester sa connexion Internet
```bash
python main.py
[4] → [1]
```

---

**Prêt à commencer? Lancez `python main.py` ! 🚀**