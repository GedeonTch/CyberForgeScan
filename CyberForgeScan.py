"""import re
import os,shutil
import stat
from datetime import datetime
import time
import string
import random
from random import randint
import pyttsx3
from pytube import Youtube
from fpdf import FPDF
import speedtest
from tqdm import tqdm
import ollama
 
def progres():
    for i in tqdm(range(100)):
        time.sleep(0.03)
progres()

from datetime import datetime
import stat
import os
import time
import shutil

def informations(chemin):
    foundInfo = 0
    
    for root, dirs, files in os.walk(chemin):
        for fichier in files:
             if fichier.lower().endswith((".conf", ".cfg", ".config", ".ini", ".yml", ".yaml", ".xml", ".json", ".properties", ".env", ".toml", ".reg", ".plist", ".inf", ".sys", ".drv",
                ".log", ".txt", ".audit", ".evt", ".evtx", ".syslog", ".journal", ".kern", ".auth", ".secure", ".messages", ".debug", ".error", ".warn", ".info", ".trace",
                ".py", ".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd", ".js", ".php", ".java", ".c", ".cpp", ".cs", ".go", ".rb", ".pl", ".lua", ".sql", ".r", ".m",
                ".html", ".htm", ".js", ".css", ".php", ".asp", ".aspx", ".jsp", ".war", ".jar", ".pcap", ".cap", ".har", ".htaccess", ".htpasswd", ".robots.txt",
                ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".bak", ".backup", ".old", ".temp", ".tmp", ".swp","mp4","mp3")): 
                try:
                    chemin_complet = os.path.join(root, fichier)
                    info = os.stat(chemin_complet)
                    
                    print(f"NOM {fichier}")
                    print(f"DOSSIER: {root}")
                    
                    # ✅ AMÉLIORATION : Affiche en Ko si < 1 MB
                    taille_octets = info.st_size
                    
                    if taille_octets < 1024:  #  1 Octet
                        print(f"Taille: {taille_octets} octets")
                        print(f"Dernière accès🕚:{datetime.fromtimestamp(info.st_atime)}")
                        print(f"Derniere modification📝:{datetime.fromtimestamp(info.st_mtime)}")
                        print(f"les droits:->{stat.filemode(info.st_mode)}\n\n")
                    elif taille_octets < 1024 * 1024:  # < 1 MB
                        taille_ko = taille_octets / 1024
                        print(f"Taille: {taille_ko:.2f} Ko")
                        print(f"Taille: {taille_octets} octets")
                        print(f"Dernière accès🕚:{datetime.fromtimestamp(info.st_atime)}")
                        print(f"Derniere modification📝:{datetime.fromtimestamp(info.st_mtime)}")
                        print(f"les droits:->{stat.filemode(info.st_mode)}\n\n")
                    else:  # >= 1 MB
                        taille_mb = taille_octets / (1024 * 1024)
                        print(f"Taille: {taille_mb:.2f} MB")
                        print(f"Taille: {taille_octets} octets")
                        print(f"Dernière accès🕚:{datetime.fromtimestamp(info.st_atime)}")
                        print(f"Derniere modification📝:{datetime.fromtimestamp(info.st_mtime)}")
                        print(f"les droits:->{stat.filemode(info.st_mode)}\n")

                    foundInfo += 1
                    
                except Exception as e:
                    print(f"Erreur: {e}")           
    if foundInfo > 0:
        print(f"{foundInfo} fichiers trouvés et analysés\n") 
        print("-"*150)
    else: 
        print("AUCUN FICHIER TROUVE")

def lister_gros_fichier(path):
    grosFichier=None
    tailleMax=0
                    
    for root,_,files in os.walk(path):
        for fichier in files:
            #chemin=os.path.join(root,fichier)
            #taille=os.path.getsize(chemin)
            chemin= os.path.join(root, fichier)
            try:
                infos=os.stat(chemin)
                taille=infos.st_size
                if taille > tailleMax:
                    tailleMax=taille
                    grosFichier=chemin
            except Exception as e:
                print(f"Une Erreur sur {chemin} est servenue de type {e}")
    if grosFichier:
        print(f"Le Fichier le plus volumineux est {grosFichier}")
        tailleMb=tailleMax / (1024*1024)
        print(f"Sa taille est de: {tailleMb:.2f}Mo")
        print(f"Dernière accès🕚:{datetime.fromtimestamp(infos.st_atime)}")
        print(f"Derniere modification📝:{datetime.fromtimestamp(infos.st_mtime)}")
        print(f"les droits:->{stat.filemode(infos.st_mode)}\n\n")
    else:
        print("Aucun fichier trouvé")

def scanner_dossier(path):
    countFile=0
    countDir=0
    for element in os.listdir(path):
        full_path = os.path.join(path, element)
        if os.path.isfile(full_path):
            print(f"{element} est un fichier 🧾📘")
            countFile+=1
        elif os.path.isdir(full_path):
            print(f"{element} est un dossier 📂📁")
            countDir+=1

    print("\n         ","_"*7)
    print("         |RESULTAT:|")
    print("         ","°"*7)
    print(f"{countFile} fichiers trouvés\n{countDir} Dossiers Trouvés")

def all_rename(chemin,name_file):
    if not os.path.isdir(chemin):
        print("invalide")
        exit()                         
    try:
        for i,fichier in enumerate(os.listdir(chemin)):
            extension=os.path.splitext(fichier)[1]
            os.rename(f"{chemin}/{fichier}",f"{chemin}/{name_file}_{i}{extension}")
            print("done")
    except Exception as e:
        print(e)

def organiser_fichiers(dossier):
    if not os.path.isdir(dossier):
        print("ERREUR, c'est pas un dossier❌")
        exit()
    try:
        for fichier in os.listdir(dossier):
            chemin_complet=os.path.join(dossier,fichier)
            if os.path.isfile(chemin_complet):
                extension=os.path.splitext(fichier)[1].lower()
                sous_dossier= f'{dossier}/fichier_{extension}'
                if not os.path.exists(sous_dossier):
                    os.mkdir(sous_dossier)
                shutil.move(chemin_complet,os.path.join(sous_dossier,fichier))
            
        print("LES FICHIERS ONT ETES DEPLACES")
    except Exception as e:
        print(f"erreur {e}")



chemin=input("donner le chemin:")
informations(chemin)
print("         ","*"*23)
print("         |ANALYSE DE GROS FICHIERS|")
print("         ","*"*23)
time.sleep(0.2)
lister_gros_fichier(chemin)
time.sleep(0.2)
scanner_dossier(chemin) 

import os,shutil
import stat
from datetime import datetime
import time
import re
import os

def extraire_info_ligne(ligne):
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", ligne)
    ips = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", ligne)
    time = re.findall(r"\b[0-2]?[0-9]:[0-5][0-9](?:AM|PM)?\b", ligne)
    dates = re.findall(r"\b(?:[0-3]?[0-9][/:]){2}[0-9]{2,4}\b", ligne)
    return emails, ips, time, dates
 
def analyser_fichier_log(chemin):
    sensibles=["error", "permission", "admin", "root", "hack", "access", "denied", "granted"]
    listeSensible=""
    emails, ips, times, dates = [], [], [], []
    full_path2=os.path.join(chemin)
    fichier=full_path2
    if fichier.endswith((".txt",".log")):
        try:
            with open(fichier, "r", encoding="utf-8") as f:
                for ligne in f:
                    e, i, t, d = extraire_info_ligne(ligne)
                    emails.extend(e)
                    ips.extend(i)
                    times.extend(t)
                    dates.extend(d)
                    with open("Extraction_Analyse.txt","a") as f:
                        f.writelines(f"Nom du Fichier: {full_path2}")
                        f.writelines(f"Email: {emails}\nIps:{ips}\nDate:{dates}\nHeures:{times}")
                    
                    ligne_lower = ligne.lower()
                    for mot in sensibles:
                        if mot.lower() in ligne_lower.lower():
                            print(f"ALERTE: {mot} détecté dans {fichier}")
                            print(f"   Contenu: {ligne.strip()[:100]}...")
                            print("-" * 40)
                            listeSensible+=mot
                        
                print("les resulats sont stockés dans le fichier Extraction_Analyse.txt")

        except FileNotFoundError:
            print("Fichier introuvable:", fichier)
        except Exception as e:
            print(f"Une erreur de type -' {e} '- s'est produite")
    return emails, ips, times, dates,listeSensible



def afficher(emails,ips,heures,dates,listeSensible):

    all_emails,all_ips,all_times,all_dates,motsSensibles=analyser_fichier_log(chemin)
    if listeSensible:
        print("⚠️❌ Mot sensible trouvé")
        for liste in listeSensible:
            print(f"   •{liste} ")
    if emails:
        print(f"📧 Emails trouvés ({len(emails)}):")
        for email in emails:
            print(f"   • {email}")
    else:
        print("NO MAIL FOUND")
    if ips:
        print(f"IPS FOUND({len(ips)})")
        for ip in ips:
            print(f"    • {ip}")
    else:
        print("NO IP FOUND")
    if time:
        print(f"HOURS FOUNDS{len(heures)} ")
        for hour in heures:
            print(f"    • {hour}")
    else: print("NO HOURS FOUND")
    if dates:
        print(f"DATES FOUND ({len(dates)})")
        for date in dates:
            print(f"     • {date}")
    else: print("NO DATES FOUND")
    print("-" * 50)
    print(f"Mots sensibles trouvés: {motsSensibles}")
    print(f"Emails trouvés: {all_emails}")
    print(f"IPs trouvées: {all_ips}")
    print(f"Heures trouvées: {all_times}")
    print(f"Dates trouvées: {all_dates}")
    print("-" * 50) 

    print("\n" + "✅" * 15)
    print("RÉSUMÉ FINAL:")
    print(f"Mots sensibles trouvés: {listeSensible}")
    print(f"  • Emails: {len(emails)}")
    print(f"  • Adresses IP: {len(ips)}")
    print(f"  • Heures: {len(heures)}")
    print(f"  • Dates: {len(dates)}")
    print("✅" * 15)

if __name__=="__main__":
    chemin=input("Entrer le chemin du fichier à analyser:  ").strip()
    analyser_fichier_log(chemin)
    emails,ips,heures,dates,sensibles=analyser_fichier_log(chemin)
    afficher(emails,ips,heures,dates,sensibles)


import random
import time
import string
import secrets
def generatePswdWithInfo(code,longeur):
    #string.printable #tous les characteres(chiffre,lettre,char)
    for i in range(1,6):
        
        maj=string.ascii_uppercase
        min=string.ascii_lowercase
        chiffres=string.digits
        special=string.punctuation
        characteres=maj+min+chiffres+special
        password=code+"".join(secrets.choice(characteres) for _ in range(longeur))
        #code+''.join(random.choice(characteres) for _ in range(longeur-len(code)))
        
        print(f"traitement en cours du mot de passe {i}")
        time.sleep(1)
        print(f'code géneré {i}:->  {password}')
        with open("mot de passe.txt","a") as f:
            f.writelines(f"mots de passe moyen{i}: {password}|\n")
    print("\n")
    print("             ","-"*25) 
    print("             | CODE TRES FORT EN COURS |")
    print("             ","-"*25) 
    print("\n")
    for i in range(1,5):
        mps_fort=''.join(random.sample(password, len(password)))
        print(f"traitement en cours du mot de passe {i}")
        time.sleep(1)
        print(f"{i}:->  {mps_fort}")
        with open("mot de passe.txt","a") as f:
            f.writelines(f"mot de passe fort{i}: {mps_fort}\n")
    print("\n")
    print("-"*83)
    print("| les mots de passe sont enregistrés avec succès dans le fichier MOT DE PASSE.txt |")
    print("-"*83) 
    print("\n\n")

def passWordTest(password):
    
    sensible=["admin".lower(),"azerty","qwerty","123456789"]
    valide=(len(password) >=8 and password[0].isupper() and any(a.isalpha() for a in password) and any(d.isdigit() for d in password) and not "1234" in password 
            and not any(sens in password for sens in sensible) and any(char in password for char in string.punctuation))
    if valide :
        print(f"MOT DE PASSE {password} FORT")
    elif any(sens in password for sens in sensible):
        print("presence d'un mot sensible dans vos données")
    else:
        print("Vos donneées sont éronnées, vous devez respecter les règles pour un mot de passe fort\n(LETTRE MAJ AU DEBUT, CHIFFRE,CHARACTER SPECIAL)")
    print("\n\n")
def genateStrong_WithoutInfo(length=16):
    if length<4:
        raise ValueError("Doit etre superieur à 4")
    maj=string.ascii_uppercase
    min=string.ascii_lowercase
    chiffres=string.digits
    special=string.punctuation

    Guaranted=[
        secrets.choice(maj), secrets.choice(min),secrets.choice(chiffres),secrets.choice(special)
    ]
    total=maj+min+chiffres+special
    rest= [secrets.choice(total) for _ in range(length-4)]
    password=Guaranted+rest
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def shutDown(choix):
    while True:
        try:
            print("Pour éteindre votre PC, tapez un chiffre entre 1 et 9, si non tapez 0")
            choix=int(input(">"))
            if choix != 0:
                print("Merci")
                break
            else:
                print("la machine va s'éteindre")
                os.system("shutdown /s /t 5")
        except ValueError:
            print("vous devez entrer un entier")

# Liste des phrases à dire
engine = pyttsx3.init()
engine.setProperty('voice','french')
phrases = [
    "BIENVENU DANS VOTRE OUTIL D'ANALYSE ET D'EXTACTION\n"
    f"CET OUTIL VOUS PERMET DE SCANNER LE DOSSIER POUR L'ANALYSE📁📂📝,L'EXTRACTION DES DONNEES DANS VOS FICHIERS⬇️➡️🆗\n"
    "CET OUTIL VOUS PERMET DE SCANNER LE DOSSIER POUR L'ANALYSE📁📂📝,L'EXTRACTION DES DONNEES DANS VOS FICHIERS⬇️➡️🆗\n"
    "MOT DE PASSE ET AUTRE🔒🔐), TESTER VOTRE CONNEXION INTERNET📶🛜📩🆗\n TELECHARGER LES VIDEOS VIA YOUTUBE ET COVERTURE VIS FICHIERS\n"
    "GERER VOS DONNEES (MOT DE PASSE ET AUTRE🔒🔐), TESTER VOTRE CONNEXION INTERNET📶🛜📩🆗\n TELECHARGER LES VIDEOS VIA YOUTUBE ET COVERTURE VIS FICHIERS\n"
    "CHAQUE PARTIE CONTIENT SES PROPRES MODULES\n"
    "CHAQUE PARTIE CONTIENT SES PROPRES MODULES\n"
    "PARTIE 1,ANALYSE DES FICHIERS\n"
    "Module 1:SCANNER LE DOSSIER.\nModule 2:VOIR LES INFO DU FICHIER,(Date de création,taille,droits)\n"
    "module 3: ARRANGER LES FICHIERS D'UN DOSSIER PAR EXTENSION\n"
    "module 4: RENOMMER AUTOMATIQUEMENT TOUS LES FICHIERS D'UN DOSSIER\n"
    "Module 5: LISTER LES GROS FICHIERS\n"
]
print("🔊 Début de la lecture...")

#for i, phrase in enumerate(phrases, 1):
phrases = engine.getProperty('voices')
for phrase in phrases:
    if 'french' in phrase.name.lower() or 'fr' in phrase.id.lower():
        engine.setProperty('voices', phrase.id)
        break
    print(f"{phrase}")
    engine.say(phrase)
    engine.runAndWait()  
    # ⬅️ BLOCANT - attend la fin
print("✅ Toutes les phrases ont été lues")



print("--_--_--_POINT 2--_--_--_EXTRACTION")
print("Module 1:EXTRAIRE LES DONNEES DANS UN FICHIER(gmail,IP,Date,Heures,Mots sensibles)\n")
print("Module 2: EXTRAIRE LES INFORMATIONS DES WIFI ENREGISTRES SUR VOTRE APPAREIL")


print("--_--_--_POINT 3--_--_--_TELECHARGEMENT,CONVERSION ET GESTION DE MOT DE PASSE")
print("Module1: TESTER LA VITESSE DU TELECHARGEMENT 🚀💫☑️🔜🛜📶🌐✅❎")
print("Module 2: TELECHERGER UNE VIDEO SUR YOUTUBE GRATUITEMENT📩✅🛜📶🆗")
print("Module3: TESTER SI TON MOT DE PASSE PEUT RESISTER AUX ATTAQUES🔐💀⚡")
print("Module 4: PROPOSER UNE LISTES DES MOTS DE PASSE FORT SUR BASE DES TES INFORMATIONS ET LES ENREGISTER DANS UN FICHIER AUTOMATIQUEMENT🔒🔐")
print("Module 6: CONERTIR UN FICHIER EN PDF🗃️🗄️💀")
print("Module 6:ETEINDRE TON PC DIRECTEMENT OU APRES UN DELAI💻❌")


choix_Partie=int(input("entrer la partie à séléction"))
if choix_Partie== 1:
    choix=int(input("POUR SCANNER LE DOSSIER TAPER 1\nPOUR EXTRAIRE LES DONNEES DANS UN FICHIER TAPEZ 2\nPOUR VOIR LES INFO DU FICHIER TAPEZ 3\nPOUR LISTER LES GROS FICHIERS TAPEZ 4"))
    path = input("ENTRER LE CHEMIN DU DOSSIER: ")
    sensibles = ["error", "warning", "attention", "erreur", "failed", "denied", "échoué", "refusé", "urgence", "alert"]
fichier=path
if choix==1:
    scanner_dossier(path)
elif choix==2:
    analyser_fichier_log(sensibles,fichier)
elif choix==3:
    informations(fichier,path)
elif choix==4:
    lister_gros_fichier(path)
else:
    print("CHOIX INVALIDE")
    time.sleep(0.05)
    print("GOODBYE")

print("🤖 ChatBot prêt à l'Utilisation!! Tapez 'exit' pour sortir")

while True:
    try:
        question = input("\n👤 Vous: ")
        
        if question.lower() == 'exit':
            print("👋 Au-revoir")
            break
        
        # Génère la réponse
        reponse = ollama.chat(
            model='phi',  # Modèle léger et rapide
            messages=[{'role': 'user', 'content': question}]
        )
        
        print(f"🤖 Bot: {reponse['message']['content']}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("Vérifie qu'Ollama est bien lancé !")


 
try:
    with open("main.py","a") as f:
        f.writelines("i'm a py file")
        print("done")
except FileExistsError:
    print("le fichier existe déjà")
"""
""" import pyttsx3
def parler():

    engine = pyttsx3.init()
    engine.setProperty('voice','french')
    phrases = [
    "BIENVENU DANS VOTRE OUTIL D'ANALYSE ET D'EXTACTION\n"
    f"CET OUTIL VOUS PERMET DE SCANNER LE DOSSIER POUR L'ANALYSE📁📂📝,L'EXTRACTION DES DONNEES DANS VOS FICHIERS⬇️➡️🆗\n"
    "CET OUTIL VOUS PERMET DE SCANNER LE DOSSIER POUR L'ANALYSE📁📂📝,L'EXTRACTION DES DONNEES DANS VOS FICHIERS⬇️➡️🆗\n"
    "MOT DE PASSE ET AUTRE🔒🔐), TESTER VOTRE CONNEXION INTERNET📶🛜📩🆗\n TELECHARGER LES VIDEOS VIA YOUTUBE ET COVERTURE VIS FICHIERS\n"
    "GERER VOS DONNEES (MOT DE PASSE ET AUTRE🔒🔐), TESTER VOTRE CONNEXION INTERNET📶🛜📩🆗\n TELECHARGER LES VIDEOS VIA YOUTUBE ET COVERTURE VIS FICHIERS\n"
    "CHAQUE PARTIE CONTIENT SES PROPRES MODULES\n"
    "CHAQUE PARTIE CONTIENT SES PROPRES MODULES\n"
    "PARTIE 1,ANALYSE DES FICHIERS\n"
    "Module 1:SCANNER LE DOSSIER.\nModule 2:VOIR LES INFO DU FICHIER,(Date de création,taille,droits)\n"
    "module 3: ARRANGER LES FICHIERS D'UN DOSSIER PAR EXTENSION\n"
    "module 4: RENOMMER AUTOMATIQUEMENT TOUS LES FICHIERS D'UN DOSSIER\n"
    "Module 5: LISTER LES GROS FICHIERS\n"
    ]
    print("🔊 Début de la lecture...")

#for i, phrase in enumerate(phrases, 1):
    phrases = engine.getProperty('voices')
    for phrase in phrases:
        if 'french' in phrase.name.lower() or 'fr' in phrase.id.lower():
            engine.setProperty('voices', phrase.id)
            break
        print(f"{phrase}")
        engine.say(phrase)
        engine.runAndWait()  
    # ⬅️ BLOCANT - attend la fin
    print("✅ Toutes les phrases ont été lues") """
import tqdm
