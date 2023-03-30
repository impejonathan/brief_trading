import sqlite3

connexion = sqlite3.connect("bdd.db")
curseur = connexion.cursor()

curseur.execute("""
                CREATE TABLE IF NOT EXISTS utilisateur (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    est_actif BOOLEAN NOT NULL,
                    mdp TEXT NOT NULL,
                    jwt TEXT
                )
                """)
connexion.commit()

curseur.execute("""
                CREATE TABLE IF NOT EXISTS article (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titre TEXT NOT NULL,
                    contenu TEXT NOT NULL,
                    date TEXT NOT NULL,
                    auteur_id INTEGER,
                    FOREIGN KEY (auteur_id)
                        REFERENCES utilisateur(id)
                        ON DELETE CASCADE
                )
                """)
connexion.commit()

connexion.close()