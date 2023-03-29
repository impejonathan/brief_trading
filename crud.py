import sqlite3

connexion = sqlite3.connect('db_trading.db')
curseur = connexion.cursor()


# ----------------------------Table "utilisateur" --------------------------------------

def creer_utilisateur(nom, email, mdp, token):
    curseur.execute("""
        INSERT INTO utilisateur(nom, email, mdp, token)
        VALUES(?,?,?,?)
    """, (nom, email, mdp, token))
    connexion.commit()
    return curseur.lastrowid


# creer_utilisateur("jonathan", "jonathan@gmail.com", "azerty123", "123")
 
def lire_utilisateurs():
    curseur.execute("""
        SELECT * FROM utilisateur
    """)
    utilisateurs = curseur.fetchall()
    return utilisateurs

lire_utilisateurs() 

def lire_utilisateur_par_id(id_utilisateur):
    curseur.execute("""
        SELECT * FROM utilisateur
        WHERE id=?
    """, (id_utilisateur,))
    utilisateur = curseur.fetchone()
    return utilisateur
    
def mettre_a_jour_utilisateur(id_utilisateur, nom, email, mdp, token):
    curseur.execute("""
        UPDATE utilisateur
        SET nom=?, email=?, mdp=?, token=?
        WHERE id=?
    """, (nom, email, mdp, token, id_utilisateur))
    connexion.commit()
    
def supprimer_utilisateur(id_utilisateur):
    curseur.execute("""
        DELETE FROM utilisateur
        WHERE id=?
    """, (id_utilisateur,))
    connexion.commit()
    
    
# # ----------------------------Table "action" --------------------------------------


def creer_action(prix, entreprise):
    curseur.execute("""
        INSERT INTO action(prix, entreprise)
        VALUES(?,?)
    """, (prix, entreprise))
    connexion.commit()
    return curseur.lastrowid
    
def lire_actions():
    curseur.execute("""
        SELECT * FROM action
    """)
    actions = curseur.fetchall()
    return actions
    
def lire_action_par_id(id_action):
    curseur.execute("""
        SELECT * FROM action
        WHERE id=?
    """, (id_action,))
    action = curseur.fetchone()
    return action
    
def mettre_a_jour_action(id_action, prix, entreprise):
    curseur.execute("""
        UPDATE action
        SET prix=?, entreprise=?
        WHERE id=?
    """, (prix, entreprise, id_action))
    connexion.commit()
    
def supprimer_action(id_action):
    curseur.execute("""
        DELETE FROM action
        WHERE id=?
    """, (id_action,))
    connexion.commit()


# # ----------------------------"asso_suivi_suiveur" --------------------------------------


def creer_asso_suivi_suiveur(id_suivi, id_suiveur):
    curseur.execute("""
        INSERT INTO asso_suivi_suiveur(id_suivi, id_suiveur)
        VALUES (?,?)
    """, (id_suivi, id_suiveur))
    connexion.commit()
    return curseur.lastrowid

# def lire_asso_suivi_suiveur_par_id(id_asso):
#     curseur.execute("""
#         SELECT * FROM asso_suivi_suiveur
#         WHERE id=?
#     """, (id_asso,))
#     asso = curseur.fetchone()
#     return asso

def lire_asso_suivi_suiveur_par_suivi(id_suivi):
    curseur.execute("""
        SELECT * FROM asso_suivi_suiveur
        WHERE id_suivi=?
    """, (id_suivi,))
    assos = curseur.fetchall()
    return assos

def lire_asso_suivi_suiveur_par_suiveur(id_suiveur):
    curseur.execute("""
        SELECT * FROM asso_suivi_suiveur
        WHERE id_suiveur=?
    """, (id_suiveur,))
    assos = curseur.fetchall()
    return assos


def mettre_a_jour_asso_suivi_suiveur(id_asso, id_suivi=None, id_suiveur=None):
    update_clause = ""
    update_values = []
    if id_suivi:
        update_clause += "id_suivi=?, "
        update_values.append(id_suivi)
    if id_suiveur:
        update_clause += "id_suiveur=?, "
        update_values.append(id_suiveur)
    update_clause = update_clause[:-2]
    update_values.append(id_asso)
    curseur.execute(f"""
        UPDATE asso_suivi_suiveur
        SET {update_clause}
        WHERE id=?
    """, tuple(update_values))
    connexion.commit()


def supprimer_asso_suivi_suiveur(id_asso):
    curseur.execute("""
        DELETE FROM asso_suivi_suiveur
        WHERE id=?
    """, (id_asso,))
    connexion.commit()


#  -------Table "asso_utilisateur_action"

def creer_asso_utilisateur_action(id_utilisateur, id_action):
    curseur.execute("""
        INSERT INTO asso_utilisateur_action(id_utilisateur, id_action)
        VALUES(?,?)
    """, (id_utilisateur, id_action))
    connexion.commit()
    return curseur.lastrowid
    
def lire_assos_utilisateur_action():
    curseur.execute("""
        SELECT * FROM asso_utilisateur_action
    """)
    assos_utilisateur_action = curseur.fetchall()
    return assos_utilisateur_action
    
def lire_asso_utilisateur_action_par_id(id_asso_utilisateur_action):
    curseur.execute("""
        SELECT * FROM asso_utilisateur_action
        WHERE id=?
    """, (id_asso_utilisateur_action,))
    asso_utilisateur_action = curseur.fetchone()
    return asso_utilisateur_action
    
def mettre_a_jour_asso_utilisateur_action(id_asso_utilisateur_action, id_utilisateur, id_action):
    curseur.execute("""
        UPDATE asso_utilisateur_action
        SET id_utilisateur=?, id_action=?
        WHERE id=?
    """, (id_utilisateur, id_action, id_asso_utilisateur_action))
    connexion.commit()
    
def supprimer_asso_utilisateur_action(id_asso_utilisateur_action):
    curseur.execute("""
        DELETE FROM asso_utilisateur_action
        WHERE id=?
    """, (id_asso_utilisateur_action,))
    connexion.commit()

