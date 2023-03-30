from pydantic import BaseModel
import sqlite3
import hashlib
import secrets
from typing import Optional
from fastapi import FastAPI, HTTPException
import jwt

connexion = sqlite3.connect('db_trading.db')
app = FastAPI()
# ESPACE DE TEST ---------------------------------------------------------------------------------------


# UTILISATEUR ---------------------------------------------------------------------------------------

class Utilisateur(BaseModel):
    # id : int
    nom: str
    email: str
    mdp: str
    # token: str


# @app.post("/creer_utilisateur")  # OK
# async def creer_utilisateur(utilisateur:Utilisateur):
#     curseur = connexion.cursor()
#     curseur.execute("""
#         INSERT INTO utilisateur(nom, email, mdp, token)
#         VALUES(?,?,?,?)
#     """, (utilisateur.nom, utilisateur.email, utilisateur.mdp, utilisateur.token))
#     connexion.commit()


@app.post("/creer_utilisateur")
async def creer_utilisateur(utilisateur: Utilisateur):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM utilisateur WHERE email = ?
    """, (utilisateur.email,))
    res = curseur.fetchall()

    if res:
        raise HTTPException(status_code=400, detail="Un utilisateur avec cet email existe déjà")
    else:
        # Hash du mot de passe
        mdp_hash = hashlib.sha256(utilisateur.mdp.encode()).hexdigest()

        # Création de l'utilisateur avec un token unique
        token = secrets.token_hex(16)
        curseur.execute("""
            INSERT INTO utilisateur(nom, email, mdp, token)
            VALUES (?, ?, ?, ?)
        """, (utilisateur.nom, utilisateur.email, mdp_hash, token))
        connexion.commit()

        # Renvoi de l'utilisateur avec son token
        return {"id": curseur.lastrowid, "nom": utilisateur.nom, "email": utilisateur.email, "token": token}


@app.get("/lire_utilisateurs") #OK
async def lire_utilisateurs():
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM utilisateur
    """)
    utilisateurs = curseur.fetchall()
    return utilisateurs

@app.get("/lire_utilisateur_par_id") #OK
async def lire_utilisateur_par_id(id_utilisateur:int):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM utilisateur
        WHERE id = ?
    """, (id_utilisateur,))
    utilisateur = curseur.fetchone()
    return utilisateur

@app.put("/mettre_a_jour_utilisateur") #OK
async def mettre_a_jour_utilisateur(utilisateur:Utilisateur,id_utilisateur:int):
    curseur = connexion.cursor()
    curseur.execute("""
        UPDATE utilisateur
        SET nom=?, email=?, mdp=?, token=?
        WHERE id=?
    """, (utilisateur.nom, utilisateur.email, utilisateur.mdp, utilisateur.token,id_utilisateur))
    connexion.commit()

@app.delete("/supprimer_utilisateur") #OK
async def supprimer_utilisateur(id_utilisateur:int):
    curseur = connexion.cursor()
    curseur.execute("""
        DELETE FROM utilisateur
        WHERE id=?
    """, (id_utilisateur,))
    connexion.commit()
    
    
@app.get("/valider_token")
async def valider_token(token: str):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM utilisateur WHERE token = ?
    """, (token,))
    res = curseur.fetchone()

    if res:
        # le token existe dans la base de données
        return {"validité_token": True}
    else:
        # le token n'existe pas dans la base de données
        return {"validité_token": False}

# --------------------------------------------------------------------------------------------------------------
class Action(BaseModel):

    # id : int
    prix: float
    entreprise: str

@app.post("/creer_action") #OK
async def creer_action(action : Action):
    curseur = connexion.cursor()
    curseur.execute("""
        INSERT INTO action(prix, entreprise)
        VALUES(?,?)
    """, (action.prix, action.entreprise))
    connexion.commit()
    

@app.get("/lire_actions") #OK
async def lire_actions():
    curseur = connexion.cursor()

    curseur.execute("""
        SELECT * FROM action
    """)
    actions = curseur.fetchall()
    return actions

@app.get ("/lire_action_par_id") #OK
async def lire_action_par_id(id_action:int):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM action
        WHERE id=?
    """, (id_action,))
    action = curseur.fetchone()
    return action

@app.put ("/mettre_a_jour_action") #OK
async def mettre_a_jour_action(action:Action,id_action:int):
    curseur = connexion.cursor()
    curseur.execute("""
        UPDATE action
        SET prix=?, entreprise=?
        WHERE id=?
    """, (action.prix, action.entreprise, id_action))
    connexion.commit()

@app.delete ("/supprimer_action") #OK
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
    # id_asso_utilisateur_action : int

@app.post("/creer_asso_utilisateur_action") #OK
async def creer_asso_utilisateur_action(id_asso_utilisateur_action:AssoUtilisateurAction):
    curseur = connexion.cursor()
    curseur.execute("""
        INSERT INTO asso_utilisateur_action(id_utilisateur, id_action)
        VALUES(?,?)
    """, (id_asso_utilisateur_action.id_utilisateur, id_asso_utilisateur_action.id_action))
    connexion.commit()

    
@app.get("/lire_assos_utilisateur_action") #OK
async def lire_assos_utilisateur_action():
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM asso_utilisateur_action
    """)
    assos_utilisateur_action = curseur.fetchall()
    return assos_utilisateur_action
    
@app.get("/lire_asso_utilisateur_action_par_id") #OK
async def lire_asso_utilisateur_action_par_id(id_asso_utilisateur_action:AssoUtilisateurAction):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM asso_utilisateur_action
        WHERE id_utilisateur = ? AND id_action = ?
    """, (id_asso_utilisateur_action.id_utilisateur,id_asso_utilisateur_action.id_action))
    asso_utilisateur_action = curseur.fetchone()
    return asso_utilisateur_action

@app.get("/actions_disponibles") #OK
async def actions_disponibles(max_prix: float):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT entreprise,prix FROM action WHERE prix <= ?
    """, (max_prix,))
    actions = curseur.fetchall()
    return actions
  
@app.get("/actions_possedees_non_vendues_suiveurs")
async def actions_possedees_non_vendues(id_utilisateur: int):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT id, prix, entreprise 
        FROM action 
        WHERE id IN (
            SELECT id_action 
            FROM asso_utilisateur_action 
            WHERE id_utilisateur IN (
                SELECT id_suivi 
                FROM asso_suivi_suiveur 
                WHERE id_suiveur=?
            )
        )
    """, (id_utilisateur,))
    actions = curseur.fetchall()
    return actions


# app.put("/mettre_a_jour_asso_utilisateur_action")
# def mettre_a_jour_asso_utilisateur_action(id_asso_utilisateur_action, id_utilisateur:AssoUtilisateurAction, id_action:AssoUtilisateurAction):
#     curseur = connexion.cursor()
#     curseur.execute("""
#         UPDATE asso_utilisateur_action
#         SET id_utilisateur=?, id_action=?
#         WHERE id=?
#     """, (id_utilisateur, id_action, id_asso_utilisateur_action))
#     connexion.commit()

@app.delete("/supprimer_asso_utilisateur_action")
def supprimer_asso_utilisateur_action(id_asso_utilisateur_action:AssoUtilisateurAction):
    connexion = sqlite3.connect('db_trading.db')
    curseur = connexion.cursor()
    curseur.execute("""
        DELETE FROM asso_utilisateur_action
        WHERE id_utilisateur = ? AND id_action = ?
    """, (id_asso_utilisateur_action.id_utilisateur,id_asso_utilisateur_action.id_action))
    connexion.commit()


class Asso_suivi_suiveur(BaseModel):
    id_suivi : int
    id_suiveur : int

@app.post("/creer_asso_suivi_suiveur") #OK
async def creer_asso_suivi_suiveur(utilisateur : Asso_suivi_suiveur):
    curseur = connexion.cursor()
    curseur.execute("""
        INSERT INTO asso_suivi_suiveur(id_suivi, id_suiveur)
        VALUES (?,?)
    """, (utilisateur.id_suivi, utilisateur.id_suiveur))
    utilisateurs = curseur.fetchall()
    connexion.commit()
    return utilisateurs


@app.get("/lire_asso_suivi_suiveur_par_suivi") #OK
async def lire_asso_suivi_suiveur_par_suivi(id_suivi: int):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM asso_suivi_suiveur
        WHERE id_suivi=?
    """, (id_suivi,))
    assos = curseur.fetchall()
    return assos

@app.get("/lire_asso_suivi_suiveur_par_suiveur") #OK
async def lire_asso_suivi_suiveur_par_suiveur(id_suiveur: int):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM asso_suivi_suiveur
        WHERE id_suiveur=?
    """, (id_suiveur,))
    assos = curseur.fetchall()
    return assos

# @app.put("/mettre_a_jour_asso_suivi_suiveur")
# async def mettre_a_jour_asso_suivi_suiveur(id_asso, id_suivi=None, id_suiveur=None):
#     curseur = connexion.cursor()
#     update_clause = ""
#     update_values = []
#     if id_suivi:
#         update_clause += "id_suivi=?, "
#         update_values.append(id_suivi)
#     if id_suiveur:
#         update_clause += "id_suiveur=?, "
#         update_values.append(id_suiveur)
#     update_clause = update_clause[:-2]
#     update_values.append(id_asso)
#     curseur.execute(f"""
#         UPDATE asso_suivi_suiveur
#         SET {update_clause}
#         WHERE id=?
#     """, tuple(update_values))
#     connexion.commit()


@app.get("/lire_asso_suivi_suiveur_par_suivi") #OK
async def lire_asso_suivi_suiveur_par_suivi(id_suivi: int):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM asso_suivi_suiveur
        WHERE id_suivi=?
    """, (id_suivi,))
    assos = curseur.fetchall()
    return assos






@app.delete("/supprimer_asso_suivi_suiveur") #OK
async def supprimer_asso_suivi_suiveur(id_asso:Asso_suivi_suiveur):
    connexion = sqlite3.connect('db_trading.db')
    curseur = connexion.cursor()
    curseur.execute("""
        DELETE FROM asso_suivi_suiveur
        WHERE id_suivi=? AND id_suiveur=?
    """, (id_asso.id_suivi,id_asso.id_suiveur))
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