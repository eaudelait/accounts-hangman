import random
import sys
import subprocess
import time
import hashlib
import json

# /!\ Le système de cryptage utilisé dans ce programme n'est pas sécurisé et sert uniquement d'exemple de gestion de comptes sur un fichier local.

def cree(username, password): # Créer un nouveau compte avec un nom d'utilisateur et un mot de passe crypté en SHA512 avec le module hashlib
    crypte = hashlib.sha512(password.encode()).hexdigest()
    account = {"username": username, "password": crypte, "stats": {"w": 0, "l": 0, "vies": 0}}
    return account

def delete(account, filename="users.json"): # Fonction pour supprimer le compte originel avant d'y ajouter la mise à jour.
    try:
        with open(filename, 'r') as f:
            accounts = json.load(f)
    except FileNotFoundError:
        accounts = []
    
    accounts = [existe for existe in accounts if existe["username"] != account["username"]]
    
    with open(filename, 'w') as f:
        json.dump(accounts, f, indent=2)

def save(account, statut, filename="users.json"): # Enregistrer le compte dans un fichier JSON
    try:
        with open(filename, 'r') as f:
            accounts = json.load(f)
    except FileNotFoundError: # Si le fichier n'existe pas, on définit la variable à un tableau vide
        accounts = []

    # Vérifier si l'utilisateur existe déjà
        
    if statut == "creation": # Uniquement procéder à la vérification lors de la création d'un compte, ainsi on peut mettre à jour
        for existe in accounts:
            if existe["username"].casefold() == account["username"].casefold():
                print(f"Le nom d'utilisateur '{account['username']}' existe déjà.")
                time.sleep(1)
                subprocess.run([sys.executable] + sys.argv)
        
        accounts.append(account)

        with open(filename, 'w') as f:
            json.dump(accounts, f, indent=2)
        return True
    else:
        accounts.append(account)
        with open(filename, 'w') as f:
            json.dump(accounts, f, indent=2)
        return True
    

            

def login(username, password, filename="users.json"): # Vérifier les informations de connexion, on vérifie si le mot de passe entré hashé est égal au hash du mot de passe enregistré pour l'utilisateur.
    crypte = hashlib.sha512(password.encode()).hexdigest()

    with open(filename, 'r') as f:
        accounts = json.load(f)

    for account in accounts:
        if account["username"].casefold() == username.casefold() and account["password"] == crypte:
            print("Connexion réussie.")
            return account
    print("Nom d'utilisateur ou mot de passe incorrect.")
    return None

def update(account, num, stat):
    # Mettre à jour les statistiques du pendu, le nombre de victoires, de défaites et de vies restantes en moyenne.
    if num == 0:
        account["stats"]["w"] +=stat
    elif num == 1:
        account["stats"]["l"] +=stat
    elif num == 2:
        account["stats"]["vies"] +=stat
    return account

def start():
    print("0 - QUITTER \n1 - Statistiques \n2 - Se connecter \n3 - Créer un compte\n4 - Jouer en tant qu'invité")
    rep = input("Votre choix : ")
    if int(rep) == 0:
        exit() # Quitte le programme
    elif int(rep) == 1: # Affichage des statistiques
        user = str(input("Veuillez entrer un nom d'utilisateur : "))
        with open("users.json", "r") as f:
            acc = json.load(f)
            for item in acc:
                if item["username"].casefold() == user.casefold():
                    print("Victoires: {}\nDéfaite: {}\nV/D: {}%\nMoyenne des vies conservées: {}\nParties totales : {}".format(item["stats"]["w"], # Nombre de victoires
                                                                                                                                    item["stats"]["l"], # Nombre de défaites
                                                                                                                                    item["stats"]["w"]/(item["stats"]["w"]+item["stats"]["l"])*100, # Ratio Victoires/Défaites
                                                                                                                                    item["stats"]["vies"]/(item["stats"]["w"]+item["stats"]["l"]), # Nombre de vies moyennes 
                                                                                                                                    item["stats"]["w"]+item["stats"]["l"])) # Parties totales
                    rep = input("Tapez 0 pour revenir au menu principal : ")
                    if int(rep) == 0:
                        subprocess.run([sys.executable] + sys.argv)
            else:
                print("Utilisateur introuvable.")


    elif int(rep) == 2: # Connexion
        exist = False
        while exist == False:
            user = str(input("Veuillez entrer un nom d'utilisateur : "))
            pass1 = input("Veuillez entrer un mot de passe : ")
            if login(user, pass1) == None:
                pass
            else:
                return login(user, pass1)
            
    elif int(rep) == 3: # Création de compte
        user = str(input("Veuillez entrer un nom d'utilisateur : "))
        time.sleep(0.5)
        pass1 = "2"
        pass2 = "1"
        while pass1 != pass2:
            pass1 = input("Veuillez entrer un mot de passe : ")
            pass2 = input("Confirmez votre mot de passe : ")
            if pass2 != pass1:
                print("Les deux mots de passes ne sont pas identiques !")
            save(cree(user, pass1), "creation")
            return login(user, pass1)
        
    elif int(rep) == 4: # Jouer sans compte (pas de sauvegarde de statistiques)
        return None

compte = start()

# On définit le dessin vide et avec le personnage, ainsi nous pourrons remplacer directement les lignes plus tard

pendu = [
    ["============    "],
    ["▮              "],
    ["▮              "],
    ["▮              "],
    ["▮              "],
    ["▮              "],
    ["▮              "],
    ["================"],
]

pendufin = [ # Chaque entrée dans ce tableau est une chance que le joueur pourra utiliser.
    ["============    "], #0
    ["▮       |      "], #1
    ["▮       o      "], #2
    ["▮      -+-      "], #3
    ["▮       Ʌ      "], #4  
]

# Fonction qui crée un menu de fin : on demande à l'utilisateur s'il souhaite quitter ou relancer une partie.

def end():
    print("0 - QUITTER \n1 - Relancer une partie")
    rep = input("Votre choix : ")
    if int(rep) == 0:
        exit() # Quitte le programme
    if int(rep) == 1:
        subprocess.run([sys.executable] + sys.argv) # Relance le programme

line = open('pendu.txt').read().splitlines() # Ouvre le fichier texte fourni avec les mots par lignes divisées
mot = random.choice(line) # Choisit une ligne aléatoire (mot)
mots = []
indice = []
for lettre in mot: # Convertit les lettres du mot en _ pour l'affichage visuel de l'indice
    mots.append(lettre)
    indice.append("_") 

def lecture(tab): # Lis le dessin du pendu par ligne sans guillemets.
    for i in tab:
        for j in i:
            print(j, end=" ")
        print()

def lecture2(indice): # Lis l'indice ou le mot sans guillemets ni espaces.
    print(" ".join(indice))

# print(mot) - Affiche le mot choisi aléatoirement, utile pour tester.

essais = 0
print("Bienvenue dans le pendu.") 

while True:
    lecture(pendu)
    lecture2(indice)
    print("Essai n°" + str(essais+1)) # On affiche le nombre d'essais
    reponse = input("Donnez une lettre ou un mot pour commencer : ")
    if len(reponse) > 1:
        if reponse.casefold() == mot.casefold(): # On vérifie si la réponse est le mot exact.
            print("Un seul coup ! Le mot était " + mot)
            print("Vies restantes : " + str(6-essais))
            if compte != None:
                delete(compte)
                compte = update(compte, 0, 1)
                save(update(compte, 2, 6-essais), "update")
            print("")
            end()
            break
        else:
            print("Ce n'est pas le bon mot !")
            lettre_correcte = True
            essais = essais+1
            try: # On tente de remplacer une ligne du tableau vide en une ligne du tableau avec le personnage.
                pendu[essais] = pendufin[essais]
            except IndexError: # S'il il y a une erreur (plus de ligne dans le tableau avec le personnage à mettre dans le tableau normal, cela veut dire que le nombre d'essais est épuisé et par conséquent on fait perdre l'utilisateur)
                print("Nombre d'essais épuisé ! Vous avez perdu... Dommage. \n Le mot était : " + mot)
                print("Vies restantes : " + str(6-essais))
            if compte != None:
                delete(compte)
                save(update(compte, 1, 1), "update")

    if len(reponse) == 1:
        lettre_correcte = False  # On ajoute une variable pour suivre si une lettre est correcte
        lettre_deja_trouvee = False  # Nouvelle variable pour suivre si la lettre a déjà été trouvée
        for i, x in enumerate(mots):
            if x.casefold() == reponse.casefold():
                if indice[i] == "_":  # Vérifier si la lettre n'a pas déjà été trouvée
                    print("Cette lettre est contenue dans le mot.")
                    indice[i] = mots[i]
                    lettre_correcte = True  # Mettre la variable à True si la lettre est correcte (empêche le message)
                else:
                    lettre_deja_trouvee = True  # Mettre la variable à True si la lettre a déjà été trouvée
        if lettre_correcte:
            if indice == mots: # Si l'indice est égal au mot, l'utilisateur a trouvé toutes les lettres donc gagne.
                print("Bravo ! Le mot était " + mot)
                print("Vies restantes : " + str(6-essais))
                if compte != None:
                    delete(compte)
                    compte = update(compte, 0, 1)
                    save(update(compte, 2, 6-essais), "update")
                time.sleep(1) # délai de 1s pour la lisiblité
                end()
                run = False
        elif lettre_deja_trouvee: # si la lettre est déjà trouvée, on ignore l'entrée.
            print("Vous avez déjà trouvé cette lettre.")
            time.sleep(1) # idem

    # On déplace le message en dehors de la boucle sinon il se répète peu importe si la lettre est correcte ou non
    if not lettre_correcte:
        print("Lettre incorrecte.")
        essais +=1
        try:
            pendu[essais] = pendufin[essais]
        except IndexError:
            print("Nombre d'essais épuisé ! Vous avez perdu... Dommage. \n Le mot était : " + mot)
            print("Vies restantes : " + str(6-essais))
            if compte != None:
                delete(compte)
                save(update(compte, 1, 1), "update")
            end()
            break
        time.sleep(1)
