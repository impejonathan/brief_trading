from pydantic import BaseModel
import sqlite3
import hashlib
import secrets
from fastapi import FastAPI, HTTPException
from jose import JWTError, jwt


connexion = sqlite3.connect('db_trading.db')
app = FastAPI()


# LES CLASS ---------------------------------------------------------------------------------------
class Utilisateur(BaseModel):

    nom: str
    email: str
    mdp: str

class Action(BaseModel):

    prix: float
    entreprise: str
    
class AssoUtilisateurAction(BaseModel):
    id_utilisateur : int
    id_action : int
    
class Asso_suivi_suiveur(BaseModel):
    id_suivi : int
    id_suiveur : int


# LES POST ---------------------------------------------------------------------------------------

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


# @app.post("/creer_action") #OK
async def creer_action(action : Action):
    curseur = connexion.cursor()
    curseur.execute("""
        INSERT INTO action(prix, entreprise)
        VALUES(?,?)
    """, (action.prix, action.entreprise))
    connexion.commit()
    
    
@app.post("/creer_asso_utilisateur_action") #OK
async def creer_asso_utilisateur_action(id_asso_utilisateur_action:AssoUtilisateurAction):
    curseur = connexion.cursor()
    curseur.execute("""
        INSERT INTO asso_utilisateur_action(id_utilisateur, id_action)
        VALUES(?,?)
    """, (id_asso_utilisateur_action.id_utilisateur, id_asso_utilisateur_action.id_action))
    connexion.commit()

    
    
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

# LES READ GET ---------------------------------------------------------------------------------------

@app.get("/id_utilisateur_par_token")
def get_user_id_from_token(token):
    connexion = sqlite3.connect('db_trading.db')
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT id FROM utilisateur WHERE token = ?
    """, (token,))
    res = curseur.fetchone()

    if res:
        return res[0]
    else:
        return None





@app.get("/id_utilisateur_par_mail") #OK
def id_utilisateur_par_mail(email):
    connexion = sqlite3.connect('db_trading.db')
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT id FROM utilisateur
        WHERE email=?
    """, (email,))
    resultat = curseur.fetchone()
    if resultat:
        return resultat[0]
    else:
        return None


# @app.get("/lire_utilisateurs") #OK
async def lire_utilisateurs():
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM utilisateur
    """)
    utilisateurs = curseur.fetchall()
    return utilisateurs

# @app.get("/lire_utilisateur_par_id") #OK
async def lire_utilisateur_par_id(id_utilisateur:int):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM utilisateur
        WHERE id = ?
    """, (id_utilisateur,))
    utilisateur = curseur.fetchone()
    return utilisateur



# @app.get("/valider_token") RENDU PRIVE !!!
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



@app.get("/lire_asso_suivi_suiveur_par_suivi") #OK
async def lire_asso_suivi_suiveur_par_suivi(id_suivi: int):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM asso_suivi_suiveur
        WHERE id_suivi=?
    """, (id_suivi,))
    assos = curseur.fetchall()
    return assos


# LES PUT UPDATE ---------------------------------------------------------------------------------------


@app.put("/mettre_a_jour_utilisateur") #OK
async def mettre_a_jour_utilisateur(utilisateur:Utilisateur,id_utilisateur:int):
    curseur = connexion.cursor()
    curseur.execute("""
        UPDATE utilisateur
        SET nom=?, email=?, mdp=?, token=?
        WHERE id=?
    """, (utilisateur.nom, utilisateur.email, utilisateur.mdp, utilisateur.token,id_utilisateur))
    connexion.commit()



# @app.put ("/mettre_a_jour_action") #OK
async def mettre_a_jour_action(action:Action,id_action:int):
    curseur = connexion.cursor()
    curseur.execute("""
        UPDATE action
        SET prix=?, entreprise=?
        WHERE id=?
    """, (action.prix, action.entreprise, id_action))
    connexion.commit()


# LES DELETE  ---------------------------------------------------------------------------------------


# @app.delete("/supprimer_utilisateur") #OK
async def supprimer_utilisateur(id_utilisateur:int):
    curseur = connexion.cursor()
    curseur.execute("""
        DELETE FROM utilisateur
        WHERE id=?
    """, (id_utilisateur,))
    connexion.commit()
    
# @app.delete ("/supprimer_action") #OK
async def supprimer_action(id_action):
    curseur = connexion.cursor()
    curseur.execute("""
        DELETE FROM action
        WHERE id=?
    """, (id_action,))
    connexion.commit()
    
@app.delete("/supprimer_asso_utilisateur_action")
def supprimer_asso_utilisateur_action(id_asso_utilisateur_action:AssoUtilisateurAction):
    connexion = sqlite3.connect('db_trading.db')
    curseur = connexion.cursor()
    curseur.execute("""
        DELETE FROM asso_utilisateur_action
        WHERE id_utilisateur = ? AND id_action = ?
    """, (id_asso_utilisateur_action.id_utilisateur,id_asso_utilisateur_action.id_action))
    connexion.commit()
    
    
@app.delete("/supprimer_asso_suivi_suiveur") #OK
async def supprimer_asso_suivi_suiveur(id_asso:Asso_suivi_suiveur):
    curseur = connexion.cursor()
    curseur.execute("""
        DELETE FROM asso_suivi_suiveur
        WHERE id_suivi=? AND id_suiveur=?
    """, (id_asso.id_suivi,id_asso.id_suiveur))
    connexion.commit()
