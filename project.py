import project_functions as pf
from csv import reader
from csv import DictReader
import mysql.connector as mc
from project_functions_sql import *


maindata = dict()
compt = 0

with open('data.csv', 'r') as data:
    data_reader = DictReader(data)
    for line in data_reader:
        maindata.setdefault(compt, line)
        compt +=1



lignes_valides = dict()
lignes_non_valides = dict()
errors = dict()

# ici on parcours toutes les lignes et on verifie pour chaque les elements
#  qui sont valident ou pas et on les stocke dans des dicos
for k in maindata.keys():
    sub_errors = dict()
    # isvalid = True
    # print()
    for subk in maindata[k].keys():
        if subk.lower()   == 'numero':
            numero = pf.v_numero(maindata[k][subk])
            if numero == False:
                sub_errors.setdefault('numero', maindata[k][subk])
        elif subk.lower() == 'nom'   :
            nom = pf.v_nom(maindata[k][subk])
            if nom == False:
                sub_errors.setdefault('nom', maindata[k][subk])
        elif subk.lower() == 'prenom':
            prenom = pf.v_prenom(maindata[k][subk])
            if prenom == False:
                sub_errors.setdefault('prenom', maindata[k][subk])
        elif subk.lower() == 'date de naissance':
            naissance = pf.v_date(str(maindata[k][subk]))
            if naissance == False:
                sub_errors.setdefault('date de naissance', maindata[k][subk])
        elif subk.lower() == 'classe':
            classe = pf.v_classe(maindata[k][subk])
            if classe == False:
                sub_errors.setdefault('classe', maindata[k][subk])
        elif subk.lower() == 'note'  :
            # avant_bool = str(maindata[k][subk])
            notes = pf.recup_notes(str(maindata[k][subk]))
            # maindata[k][subk] = notes
            if notes == False:
                sub_errors.setdefault('notes', str(maindata[k][subk]))
            else:
                maindata[k][subk] = notes
    errors.setdefault(k, sub_errors)

    if numero and nom and prenom and naissance and classe and notes:
        maindata[k]['Classe'] = pf.change_classe(maindata[k]['Classe'])
        # mettre ici le formatage des naissances
        maindata[k]['Date de naissance'] = pf.change_dformat(maindata[k]['Date de naissance'])
        lignes_valides.setdefault(k, maindata[k])
    else:
        lignes_non_valides.setdefault(k, maindata[k])




# ceci est le menu de modification
def modif_menu():
    print("""
                        |   1. Modifier une ligne invalides
                        |   2. Afficher les erreurs
        MODIFICATION    |   3. Afficher les lignes invalides
                        |   4. Revenir au menu principal
                        |   5. Pour sortir
    """)
    subchoix = int(input("Faites votre choix: "))

    if subchoix == 1:
        modif_id = int(input("Entrez le numero de la ligne à modifier: ").strip())
        print("La ligne invalide est ")
        pf.affiche_invalide(lignes_non_valides, modif_id)
        tovalidate = pf.return_invalide(lignes_non_valides, modif_id)
        # print(tovalidate)
        print("Les erreurs à corriger: ")
        pf.affiche_invalide(errors, modif_id)
        tovalidate = pf.modifier(tovalidate)
        if tovalidate == False:
            print("La modification est annulée")
            modif_menu()
        else:
            # suppression de la ligne dans le dico invalide
            del lignes_non_valides[modif_id]
            lignes_valides.setdefault(modif_id, tovalidate)
            print("La ligne " + str(modif_id) + "est ajoutée aux lignes valides avec succees")
            modif_menu()
    elif subchoix == 2:
        pf.affiche_errors(errors)
        modif_menu()
    elif subchoix == 3:
        pf.affiche_info(lignes_non_valides)
        modif_menu()
    elif subchoix == 4:
        menu()
    elif subchoix == 5:
        exit()



def menu():
    try:
        print("MENU".center(180, '*'))
        print("""
            1. Afficher les lignes valides
            2. Afficher les lignes invalides
            3. Afficher une information par numero
            4. Afficher les 5 premiers
            5. Modifier une information invalides
            6. Mettre les lignes valides dans la base de donnees
            7. Afficher les infos d'une table au choix
            Ps: Mettez 0 ou un autre chiffre pour quitter
        """)
        try:
            choix = int(input("Faites votre choix: "))
        except Exception as e:
            menu()

        if choix == 1:
            print("Affichage des lignes valides".center(140, '-'))
            pf.affiche_infov(lignes_valides)
            menu()
        elif choix == 2:
            print("Affichage des lignes invalides".center(138, '-'))
            pf.affiche_info(lignes_non_valides)
            print("Voir la liste des erreurs ? yes: pour voir /no: pour aller au menu")
            mychoix = input().lower()
            if mychoix =='yes':
                pf.affiche_errors(errors)
                menu()
            else:
                menu()
        elif choix == 3:
            print("Affichage d'une information par numero".center(130, '-'))
            numero = input("Entrer le numero à afficher: ").upper().strip()
            pf.affiche_numero(lignes_valides, numero)
            menu()
        elif choix == 4:
            print("Affichage des cinq premiers".center(140, '-'))
            pf.affiche_5premiers(lignes_valides)
            menu()
        elif choix == 5:
            print("Modification des elements invalides".center(140, '-'))
            modif_menu()
        elif choix == 6:
            push_to_database(lignes_valides)
            menu()
        elif choix == 7:
            affiche_table()
            menu()
        else:
            print("Merci de votre visite".center(178, '*'))
            exit()
    except KeyboardInterrupt:
        print()
        print("Merci de votre visite".center(178, '*'))
        print()
        exit()


print("""
		   ####      ###
		  #####     ###
		 ######    ###
		#######   ###########################################
	       ########KABA PROJET EXCEL 2022 @SONATEL ACADEMY  *
		#######   ###########################################
		 ######    ###
		  #####     ###
		   ####      ###""")

menu()

# print(lignes_valides)
