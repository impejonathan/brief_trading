import sqlite3

connexion = sqlite3.connect("db_trading.db")

curseur = connexion.cursor()

curseur.execute("""
                CREATE TABLE IF NOT EXISTS utilisateur(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    email TEXT NOT NULL,
                    mdp TEXT NOT NULL,
                    token BLOB NOT NULL
                )
                
                """)


connexion.commit()


curseur.execute("""
                CREATE TABLE IF NOT EXISTS action(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prix REAL NOT NULL,
                    entreprise TEXT NOT NULL
                    
                )
                
                """)


connexion.commit()


curseur.execute("""
                CREATE TABLE IF NOT EXISTS asso_suivi_suiveur(
                    id_suivi INTEGER,
                    id_suiveur INTEGER,
                    FOREIGN KEY(id_suivi) REFERENCES utilisateur(id),
                    FOREIGN KEY(id_suiveur) REFERENCES utilisateur(id)
                    
                )
                
                """)


connexion.commit()

curseur.execute("""
                CREATE TABLE IF NOT EXISTS asso_utilisateur_action(
                    id_utilisateur INTEGER,
                    id_action INTEGER,
                    FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id),
                    FOREIGN KEY(id_action) REFERENCES action(id)
                    
                )
                
                """)


connexion.commit()