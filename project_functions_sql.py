import mysql.connector as mc


# fonction qui affiche les elements dune table choisi
def affiche_table():
    with mc.connect(option_files = "my.ini") as mydb:
        mycursor = mydb.cursor()
        mycursor.execute("SHOW TABLES")
        tables = mycursor.fetchall()
        tables = [tab[0] for tab in tables]

        for dex, tab in enumerate(tables):
            print(f"""

                    {dex + 1}. Afficher la table {tab}

            """)
        print("Appuyer 0 pour Le menu principal")
        choice = int(input("Choose a table to display:  "))

        table = tables[choice - 1]
        if table in tables:
            select_table = f""" SELECT * FROM {table} ORDER BY id_{table[:-1]}
                            """
            mycursor.execute(select_table)
            result = mycursor.fetchall()
            for x in result:
                print(x)
    affiche_table()




# ceci est la fonction qui mets les lignes valident dans la base de donnees
def push_to_database(lignes_valides:dict):
    # connection a la base de donnees
    print("Connection  à la base de donnees....")
    # mydb = mc.connect(
    #     option_files = "my.ini"
    # )
    # mycursor = mydb.cursor()
    with mc.connect(option_files = "my.ini") as mydb:
        mycursor = mydb.cursor()

        mycursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        mycursor.execute("DELETE FROM classes")
        mycursor.execute("DELETE FROM eleves")
        mycursor.execute("DELETE FROM notes")
        mycursor.execute("DELETE FROM matieres")
        mycursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        mycursor.execute("ALTER TABLE eleves AUTO_INCREMENT = 1")
        mycursor.execute("ALTER TABLE classes AUTO_INCREMENT = 1")
        mycursor.execute("ALTER TABLE notes AUTO_INCREMENT = 1")
        mycursor.execute("ALTER TABLE matieres AUTO_INCREMENT = 1")


        print('Demarrage...')
        for key in lignes_valides:
            line           = lignes_valides.get(key)
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
            moy_gen = notes.get('moyenne_generale')
            insert_moyenne = f"""INSERT INTO moyennes (id_eleve, id_classe, value) VALUES ('{id_eleve}', '{id_classe}', '{moy_gen}')"""
            # print(insert_moyenne)
            # print(id_classe, id_eleve)

            mycursor.execute(insert_moyenne)

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

                    # print('Insertion des notes...'.center(10))
                    for type in notes[matiere]:
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
    # mydb.close()

    print('FIN du programme')
