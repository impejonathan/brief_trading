from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3


connexion = sqlite3.connect('db_trading.db')
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test():
    liste = [i for i in range(100) if i%5==0]
    return{"la liste": liste}


# UTILISATEUR ---------------------------------------------------------------------------------------

class Utilisateur(BaseModel):
    id : int
    nom: str
    email: str
    mdp: str
    token: str


@app.post("/creer_utilisateur")
async def creer_utilisateur(utilisateur: Utilisateur):
    curseur = connexion.cursor()
    curseur.execute("""
        INSERT INTO utilisateur(nom, email, mdp, token)
        VALUES(?,?,?,?)
    """, (utilisateur.nom, utilisateur.email, utilisateur.mdp, utilisateur.token))
    connexion.commit()
    utilisateur.id = curseur.lastrowid
    return utilisateur


@app.get("/lire_utilisateurs")
async def lire_utilisateurs():
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM utilisateur
    """)
    utilisateurs = curseur.fetchall()
    return utilisateurs

@app.get("/lire_utilisateur_par_id")
async def lire_utilisateur_par_id(id_utilisateur:Utilisateur):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM utilisateur
        WHERE id = ?
    """, (id_utilisateur,))
    utilisateur = curseur.fetchone()
    return utilisateur

@app.put("/mettre_a_jour_utilisateur")
async def mettre_a_jour_utilisateur(id_utilisateur:Utilisateur, nom:Utilisateur, email:Utilisateur, mdp:Utilisateur, token:Utilisateur):
    curseur = connexion.cursor()
    curseur.execute("""
        UPDATE utilisateur
        SET nom=?, email=?, mdp=?, token=?
        WHERE id=?
    """, (nom, email, mdp, token, id_utilisateur))
    connexion.commit()

@app.delete("/supprimer_utilisateur")
async def supprimer_utilisateur(id_utilisateur:Utilisateur):
    curseur = connexion.cursor()
    curseur.execute("""
        DELETE FROM utilisateur
        WHERE id=?
    """, (id_utilisateur,))
    connexion.commit()

# --------------------------------------------------------------------------------------------------------------
class Action(BaseModel):

    id : int
    prix: float
    entreprise: str

@app.post("/creer_action")
async def creer_action(action : Action):
    curseur = connexion.cursor()
    curseur.execute("""
        INSERT INTO action(prix, entreprise)
        VALUES(?,?)
    """, (action.prix, action.entreprise))
    connexion.commit()
    action.id = curseur.lastrowid
    return action

@app.get("/lire_actions")
async def lire_actions():
    curseur = connexion.cursor()

    curseur.execute("""
        SELECT * FROM action
    """)
    actions = curseur.fetchall()
    return actions

@app.get ("/lire_action_par_id")
async def lire_action_par_id(id_action):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM action
        WHERE id=?
    """, (id_action,))
    action = curseur.fetchone()
    return action

@app.put ("/mettre_a_jour_action")
async def mettre_a_jour_action(id_action, prix, entreprise):
    curseur = connexion.cursor()
    curseur.execute("""
        UPDATE action
        SET prix=?, entreprise=?
        WHERE id=?
    """, (prix, entreprise, id_action))
    connexion.commit()

@app.delete ("/supprimer_action")
async def supprimer_action(id_action):
    curseur = connexion.cursor()
    curseur.execute("""
        DELETE FROM action
        WHERE id=?
    """, (id_action,))
    connexion.commit()
    
    
    
# -------------------------------------------------------------------------------------------------------------------------

class AssoUtilisateurAction(BaseModel):
    id_utilisateur : int
    id_action : int
    id_asso_utilisateur_action : int

@app.post("/creer_asso_utilisateur_action")
async def creer_asso_utilisateur_action(id_utilisateur:AssoUtilisateurAction, id_action:AssoUtilisateurAction):
    curseur = connexion.cursor()
    curseur.execute("""
        INSERT INTO asso_utilisateur_action(id_utilisateur, id_action)
        VALUES(?,?)
    """, (id_utilisateur, id_action))
    connexion.commit()
    return curseur.lastrowid
    
@app.get("/lire_assos_utilisateur_action")
async def lire_assos_utilisateur_action():
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM asso_utilisateur_action
    """)
    assos_utilisateur_action = curseur.fetchall()
    return assos_utilisateur_action
    
@app.get("/lire_asso_utilisateur_action_par_id")
def lire_asso_utilisateur_action_par_id(id_asso_utilisateur_action:AssoUtilisateurAction):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM asso_utilisateur_action
        WHERE id=?
    """, (id_asso_utilisateur_action,))
    asso_utilisateur_action = curseur.fetchone()
    return asso_utilisateur_action
    
    
# app.put("/mettre_a_jour_asso_utilisateur_action")
# def mettre_a_jour_asso_utilisateur_action(id_asso_utilisateur_action, id_utilisateur:AssoUtilisateurAction, id_action:AssoUtilisateurAction):
#     curseur = connexion.cursor()
#     curseur.execute("""
#         UPDATE asso_utilisateur_action
#         SET id_utilisateur=?, id_action=?
#         WHERE id=?
#     """, (id_utilisateur, id_action, id_asso_utilisateur_action))
#     connexion.commit()

# app.delete("/supprimer_asso_utilisateur_action")
# def supprimer_asso_utilisateur_action(id_asso_utilisateur_action):
#     curseur = connexion.cursor()
#     curseur.execute("""
#         DELETE FROM asso_utilisateur_action
#         WHERE id=?
#     """, (id_asso_utilisateur_action,))
#     connexion.commit()


class Asso_suivi_suiveur(BaseModel):
    id_suivi : int
    id_suiveur : int

@app.post("/creer_asso_suivi_suiveur")
async def creer_asso_suivi_suiveur(utilisateur : Asso_suivi_suiveur):
    curseur = connexion.cursor()
    curseur.execute("""
        INSERT INTO asso_suivi_suiveur(id_suivi, id_suiveur)
        VALUES (?,?)
    """, (utilisateur.id_suivi, utilisateur.id_suiveur))
    utilisateurs = curseur.fetchall()
    return utilisateurs


@app.get("/lire_asso_suivi_suiveur_par_suivi")
async def lire_asso_suivi_suiveur_par_suivi(id_suivi:Asso_suivi_suiveur):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM asso_suivi_suiveur
        WHERE id_suivi=?
    """, (id_suivi,))
    assos = curseur.fetchall()
    return assos

@app.get("/lire_asso_suivi_suiveur_par_suiveur")
async def lire_asso_suivi_suiveur_par_suiveur(id_suiveur:Asso_suivi_suiveur):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM asso_suivi_suiveur
        WHERE id_suiveur=?
    """, (id_suiveur,))
    assos = curseur.fetchall()
    return assos

@app.put("/mettre_a_jour_asso_suivi_suiveur")
async def mettre_a_jour_asso_suivi_suiveur(id_asso, id_suivi=None, id_suiveur=None):
    curseur = connexion.cursor()
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

@app.put("/supprimer_asso_suivi_suiveur")
async def supprimer_asso_suivi_suiveur(id_asso):
    curseur = connexion.cursor()
    curseur.execute("""
        DELETE FROM asso_suivi_suiveur
        WHERE id=?
    """, (id_asso,))
    connexion.commit()

















# @app.post("/items/")
# async def create_item(item: Item):
#     cur = conn.cursor()
#     cur.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
#     conn.commit()
#     return {"item": item}

# @app.get("/items/")
# async def read_items():
#     cur = conn.cursor()
#     cur.execute("SELECT name, price FROM items")
#     items = cur.fetchall()
#     return {"items": items}