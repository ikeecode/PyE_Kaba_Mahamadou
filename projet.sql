
/* Creation de la base de donnees */
CREATE DATABASE IF NOT EXISTS projet_python;

/* Connection a la base de donnees*/
USE projet_python;


/* Creation de la table classes */
CREATE TABLE IF NOT EXISTS classes(
  id_classe INT PRIMARY KEY AUTO_INCREMENT,
  nom_classe VARCHAR(30) NOT NULL UNIQUE
);

/* Creation de la table eleves */
CREATE TABLE IF NOT EXISTS eleves(
  id_eleve INT PRIMARY KEY AUTO_INCREMENT,
  numero VARCHAR(30) NOT NULL UNIQUE,
  nom VARCHAR(30) NOT NULL,
  prenom VARCHAR(30) NOT NULL,
  date_naissance DATE,
  id_classe INT,
  FOREIGN KEY (id_classe) REFERENCES classes(id_classe)
);

/* Creation de la table matieres */
CREATE TABLE IF NOT EXISTS matieres(
  id_matiere INT PRIMARY KEY AUTO_INCREMENT,
  nom_matiere VARCHAR(30) NOT NULL UNIQUE
);

/* Creation de la table notes */
CREATE TABLE IF NOT EXISTS notes(
  id_note INT PRIMARY KEY AUTO_INCREMENT,
  value FLOAT,
  type ENUM('devoirs', 'examen', 'moyenne'),
  id_matiere INT,
  id_eleve INT,
  FOREIGN KEY (id_matiere) REFERENCES matieres(id_matiere),
  FOREIGN KEY (id_eleve) REFERENCES eleves(id_eleve)
);

/*
NB: note que:
type ENUM('devoir', 'examen', 'moyenne'), n'est pas dans notre table qui
est dans mysql alors faut penser le mettre a jour et voir comment inserer
la moyenne generale et ou la mettre

 */
