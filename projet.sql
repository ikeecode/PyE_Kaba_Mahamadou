/*suppression de la base */
DROP DATABASE IF EXISTS projet_python;

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
  value FLOAT DEFAULT 0,
  type ENUM('devoirs', 'examen', 'moyenne'),
  id_matiere INT,
  id_eleve INT,
  FOREIGN KEY (id_matiere) REFERENCES matieres(id_matiere),
  FOREIGN KEY (id_eleve) REFERENCES eleves(id_eleve)
);

CREATE TABLE IF NOT EXISTS moyennes(
  id_eleve INT,
  id_classe INT,
  value FLOAT NOT NULL DEFAULT 0,
  FOREIGN KEY (id_eleve) REFERENCES eleves(id_eleve),
  FOREIGN KEY (id_classe) REFERENCES classes(id_classe),
  PRIMARY KEY (id_eleve, id_classe)
);

/*
NB: note que:
type ENUM('devoir', 'examen', 'moyenne'), n'est pas dans notre table qui
est dans mysql alors faut penser le mettre a jour et voir comment inserer
la moyenne generale et ou la mettre

 */

/* calculer la moyenne des devoirs et ou examen chacun à part */


DELIMITER |

CREATE PROCEDURE moyenne_eleve (IN id INT, IN typo VARCHAR(10), OUT output FLOAT)
BEGIN
  SELECT AVG(value) INTO output FROM projet_python.notes WHERE id_eleve = id AND type = typo;
END|
/*
CREATE TRIGGER insertion_moyenne_eleve AFTER INSERT ON notes
FOR EACH ROW
BEGIN
  CALL moyenne_eleve(notes.id_eleve, 'devoirs', @devoir);
  CALL moyenne_eleve(notes.id_eleve, 'examen', @examen);
  INSERT INTO moyennes SET value = (SELECT (@devoir + 2 * @examen) / 3) WHERE moyennes.id_eleve = notes.id_eleve;
END|
*/
CREATE TRIGGER update_moyenne_eleve AFTER UPDATE ON projet_python.notes
FOR EACH ROW
BEGIN
  CALL moyenne_eleve(notes.id_eleve, 'devoirs', @devoir);
  CALL moyenne_eleve(notes.id_eleve, 'examen', @examen);
  UPDATE projet_python.moyennes SET moyennes.value = (SELECT (@devoir + 2 * @examen) / 3) WHERE moyennes.id_eleve = notes.id_eleve;
END|

DELIMITER ;
