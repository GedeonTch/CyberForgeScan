def collecter_feedback():
    
    print("\n" + "★"*50)
    print("PARTAGEZ VOTRE EXPÉRIENCE")
    print("★"*50)
    
    reponse = input("\nSouhaitez-vous laisser un commentaire sur notre service ? (oui/non) : ")
    reponses=['oui', 'o', 'yes', 'y']
    for reponse in reponses:
        if reponse.lower() :
            print("\nNous vous remercions pour votre contribution !")
            print("Vous pouvez nous contacter via :")
            print("\n" + "─" * 40)
            print("📞  Téléphone :")
            print("    • +257 66504165")
            print("\n✉️  Email :")
            print("    • tchibanvunyagedeon@gmail.com")
            print("─" * 40)
        
            print("\n📋  Types de retours attendus :")
            print("    ✓ Suggestions d'amélioration")
            print("    ✓ Signalement de problèmes")
            print("    ✓ Témoignages d'expérience")
            print("    ✓ Demandes de fonctionnalités")
        
            print("\n⏱️  Délai de traitement : 24-48 heures ouvrables")
            print("Nous vous répondrons personnellement.")

        else:
            print("\nMerci de votre confiance ! N'hésitez pas à nous contacter")
            print("ultérieurement si besoin.")
    
        print("\n" + "★"*50)

""" 
#ANONYMOUS
1
class Etudiant: #Classe principale
    def __init__(self,nom,note):
        self.nom=nom
        self.note=note
        #Déclaration des attributs et initialisation
def main():
    etudiant =[]# Initialisation de la liste etudiant
    while True:# Boucle infinie p
        try: #gestion d'erreurs
            nom=input("Entrer le nom de l'Etudiant:")
            note=float(input("ENTRER LA NOTE:"))
            etudiant.append(Etudiant(nom,note)) #ajout d'éléments dans 
                #la liste etudiant initialisée
        except ValueError as e:#capture d'erreur(string au lieu de int ou float)
            print(f"Une erreur du type {e} s'est produite")
            break#casse la boucle
        print("___---LISTE DES ETUDIANTS:---___")
        for i,student in enumerate(etudiant):#boucle pour enumer et afficher par element
            print(f"{i}. {student.nom}--> {student.note}") #Affichage
if __name__=="__main__":#entree principale
    main()#appelle de la fonction """

""" 
2
class Produit:
    def __init__(self,nom,prix):
        self.nom=nom
        self.prix=prix
def main():
    produits=[]#Liste initialisée
    produits.append(Produit("HP",250))#Ajout d'elements dans la liste
    #avec append
    produits.append(Produit("DELL",200))
    
    print("---___DETAILS DES PRODUITS---___")
    for i,produit in enumerate(produits):
        print(f"{i+1}. {produit.nom}---{produit.prix}")
if __name__=="__main__":
    main()
 """