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

/* Creation de la table moyennes */
CREATE TABLE IF NOT EXISTS moyennes(
  id_eleve INT,
  id_classe INT,
  value FLOAT NOT NULL DEFAULT 0,
  FOREIGN KEY (id_eleve) REFERENCES eleves(id_eleve),
  FOREIGN KEY (id_classe) REFERENCES classes(id_classe),
  PRIMARY KEY (id_eleve, id_classe)
);


DELIMITER |

/* Procedure qui calcule la moyenne d'un eleve en renseignant son id*/
create procedure moyenne_eleve(IN id INT, OUT output FLOAT)
  BEGIN
    DECLARE dev, exam FLOAT DEFAULT 0.0;
    SELECT AVG(value) INTO dev FROM projet_python.notes WHERE id_eleve = id AND type = 'devoirs';
    SELECT AVG(value) INTO exam FROM projet_python.notes WHERE id_eleve = id AND type = 'examen';
    SELECT (dev + 2*exam) /3 INTO output;
  END|

/* Trigger qui met à jour la moyenne quand on change une note*/
CREATE TRIGGER update_moyenne_eleve AFTER UPDATE ON projet_python.notes
FOR EACH ROW
BEGIN
  CALL moyenne_eleve(NEW.id_eleve, @moy);
  UPDATE projet_python.moyennes SET value = @moy WHERE moyennes.id_eleve = NEW.id_eleve;
END|

DELIMITER ;
