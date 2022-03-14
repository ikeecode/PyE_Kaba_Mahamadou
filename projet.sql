
/* Creation de la base de donnees */
CREATE DATABASE IF NOT EXISTS projet_python1;

/* Connection a la base de donnees*/
USE projet_python1;


/* Creation de la table classes */
CREATE TABLE IF NOT EXISTS classes(
  nom_classe VARCHAR(30) NOT NULL PRIMARY KEY
);

/* Creation de la table eleves */
CREATE TABLE IF NOT EXISTS eleves(
  numero VARCHAR(30) NOT NULL PRIMARY KEY,
  nom VARCHAR(30) NOT NULL,
  prenom VARCHAR(30) NOT NULL,
  date_naissance DATE,
  nom_classe VARCHAR(30),
  FOREIGN KEY (nom_classe) REFERENCES classes(nom_classe)
);

/* Creation de la table matieres */
CREATE TABLE IF NOT EXISTS matieres(
  nom_matiere VARCHAR(30) NOT NULL PRIMARY KEY
);

/* Creation de la table notes */
CREATE TABLE IF NOT EXISTS notes(
  id_note INT PRIMARY KEY AUTO_INCREMENT,
  value FLOAT,
  type ENUM('devoirs', 'examen', 'moyenne'),
  nom_matiere VARCHAR(30),
  numero_eleve VARCHAR(30),
  FOREIGN KEY (nom_matiere) REFERENCES matieres(nom_matiere),
  FOREIGN KEY (numero_eleve) REFERENCES eleves(numero)
);

CREATE TABLE IF NOT EXISTS moyennes(
  numero_eleve VARCHAR(30),
  nom_classe  VARCHAR(30),
  value FLOAT NOT NULL DEFAULT 0,
  FOREIGN KEY (nom_classe) REFERENCES classes(nom_classe),
  FOREIGN KEY (numero_eleve) REFERENCES eleves(numero),
  PRIMARY KEY (numero_eleve, nom_classe)
)

/*
NB: note que:
type ENUM('devoir', 'examen', 'moyenne'), n'est pas dans notre table qui
est dans mysql alors faut penser le mettre a jour et voir comment inserer
la moyenne generale et ou la mettre

 */
