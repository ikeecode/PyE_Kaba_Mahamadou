import project_functions as pf
from csv import reader
from csv import DictReader
import mysql.connector as mc



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



# ceci est la fonction qui mets les lignes valident dans la base de donnees
def push_to_database():
    # connection a la base de donnees
    print("Connection  à la base de donnees....")
    mydb = mc.connect(
        option_files = "my.ini"
    )
    mycursor = mydb.cursor()

    mycursor.execute("DELETE FROM eleves")
    mycursor.execute("DELETE FROM classes")
    mycursor.execute("DELETE FROM notes")
    mycursor.execute("DELETE FROM matieres")

    mycursor.execute("ALTER TABLE eleves AUTO_INCREMENT = 1")
    mycursor.execute("ALTER TABLE classes AUTO_INCREMENT = 1")
    mycursor.execute("ALTER TABLE notes AUTO_INCREMENT = 1")
    mycursor.execute("ALTER TABLE matieres AUTO_INCREMENT = 1")


    print('Demarrage...')
    for key in lignes_valides:
        line           = lignes_valides[key]
        numero         = line.get('Numero')
        nom            = line.get('Nom')
        prenom         = line.get('Prenom')
        date_naissance = line.get('Date de naissance')
        classe         = line.get('Classe')
        notes          = line.get('Note')
        try:
            # print('Insertion des classes...'.center(10))
            # insertion des classes
            mycursor.execute(f"INSERT INTO classes (nom_classe) VALUES ('{classe}')")
        except:
            pass
        mycursor.execute(f"SELECT id_classe FROM classes WHERE nom_classe = '{classe}'")
        id_classe = mycursor.fetchone()[0]

        # print('Insertion des eleves...'.center(10))
        # insertion des informations de l'eleve
        insert_eleve = f"""INSERT INTO eleves (numero, nom, prenom, date_naissance, id_classe)
                           VALUES ('{numero}', '{nom}', '{prenom}', '{date_naissance}', '{id_classe}')
                        """
        mycursor.execute(insert_eleve)

        # recuperation de l'id_eleve
        mycursor.execute(f"SELECT id_eleve FROM eleves WHERE numero = '{numero}'")
        id_eleve = mycursor.fetchone()[0]
        #manage notes
        # print(notes)
        for matiere in notes:
            if matiere != 'moyenne_generale':
                # print(matiere, notes[matiere])
                try:
                    # print('Insertion des matieres...'.center(10))
                    # insertion des matieres
                    mycursor.execute(f"INSERT INTO matieres (nom_matiere) VALUES ('{matiere}')")
                except:
                    pass
                mycursor.execute(f"SELECT id_matiere FROM matieres WHERE nom_matiere = '{matiere}'")
                id_matiere = mycursor.fetchone()[0]
                # print(matiere, id_matiere)

                for type in notes[matiere]:
                    # print('Insertion des notes...'.center(10))
                    # insertion examen et moyenne dans la table notes
                    if type != 'devoirs':
                        value = notes[matiere][type]
                        insert_note = f"""INSERT INTO notes (value, type, id_matiere, id_eleve)
                                          VALUES ('{value}', '{type}', '{id_matiere}', '{id_eleve}')
                                       """
                        mycursor.execute(insert_note)
                    else:
                        # insertion des devoirs dans la table notes
                        devoirs = notes[matiere][type]
                        for value in devoirs:
                            insert_note = f"""INSERT INTO notes (value, type, id_matiere, id_eleve)
                                              VALUES ('{value}', '{type}', '{id_matiere}', '{id_eleve}')
                                           """
                            mycursor.execute(insert_note)

    mydb.commit()
    mydb.close()

    print('FIN du programme')




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
        print("MENU".center(183, '*'))
        print("""
            1. Afficher les lignes valides
            2. Afficher les lignes  invalides
            3. Afficher une information par numero
            4. Afficher les 5 premiers
            5. Modifier une information invalides
            6. Mettre les lignes valides dans la base de donnees
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
            push_to_database()
            menu()
        else:
            print("Merci de votre visite".center(183, '*'))
            exit()
    except KeyboardInterrupt:
        print()
        print("Merci de votre visite".center(183, '*'))
        print()
        exit()


print("""
		   ####      ###
		  #####     ###
		 ######    ###
		#######   #######################################
	       ########ABA PROJET EXCEL 2022 @SONATEL ACADEMY   *
		#######   #######################################
		 ######    ###
		  #####     ###
		   ####      ###""")

menu()

# print(lignes_valides)
