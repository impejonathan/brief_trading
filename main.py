from pydantic import BaseModel
import sqlite3
import hashlib
import secrets
from fastapi import FastAPI, HTTPException,Header

connexion = sqlite3.connect('db_trading.db')
app = FastAPI(openapi_url="/openapi.json", docs_url="/")



async def get_user_id_from_token(token: str):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT id FROM utilisateur
        WHERE token=?
    """, (token,))
    resultat = curseur.fetchone()
    if resultat is None:
        raise HTTPException(status_code=401, detail="Token invalide")
    return resultat[0]


# LES CLASS ---------------------------------------------------------------------------------------
class Utilisateur(BaseModel):

    nom: str
    email: str
    mdp: str
    
class Action(BaseModel):

    prix: float
    entreprise: str
    
class ActionPrix(BaseModel):
    prix: float
    
class AssoUtilisateurAction(BaseModel):
    id_utilisateur : int
    id_action : int
    
class Asso_suivi_suiveur(BaseModel):
    id_suivi : int
    id_suiveur : int

class DeleteAction(BaseModel):
    entreprise : str

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


#@app.post("/creer_action") #OK
async def creer_action(action : Action):
    curseur = connexion.cursor()
    curseur.execute("""
        INSERT INTO action(prix, entreprise)
        VALUES(?,?)
    """, (action.prix, action.entreprise))
    connexion.commit()
    
    
@app.post("/creer_asso_utilisateur_action")
async def creer_asso_utilisateur_action(id_action: int, authorization: str = Header("Authorization")):
    connexion = sqlite3.connect('db_trading.db')

    curseur = connexion.cursor()

    # Récupération de l'id de l'utilisateur à partir du token JWT
    id_utilisateur = await get_user_id_from_token(authorization)

    curseur.execute("""
        INSERT INTO asso_utilisateur_action(id_utilisateur, id_action)
        VALUES (?,?)
    """, (id_utilisateur, id_action))
    connexion.commit()

    return {"id_utilisateur": id_utilisateur, "id_action": id_action}



    
    
@app.post("/creer_asso_suivi_suiveur")
async def creer_asso_suivi_suiveur(id_suivi: int, authorization: str = Header("Authorization")):
    connexion = sqlite3.connect('db_trading.db')
    curseur = connexion.cursor()

    # Récupération de l'id de l'utilisateur à partir du token JWT
    id_suiveur = await get_user_id_from_token(authorization)

    curseur.execute("""
        INSERT INTO asso_suivi_suiveur(id_suivi, id_suiveur)
        VALUES (?,?)
    """, (id_suivi, id_suiveur))
    connexion.commit()

    return {"id_suivi": id_suivi, "id_suiveur": id_suiveur}

# LES READ GET ---------------------------------------------------------------------------------------

@app.get("/id_utilisateur_par_token") #OK A CHANGER
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





@app.get("/id_utilisateur_par_mail") #OK A CHANGER
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



# LES PUT UPDATE ---------------------------------------------------------------------------------------


# @app.put("/mettre_a_jour_utilisateur") #OK
# async def mettre_a_jour_utilisateur(utilisateur:Utilisateur,id_utilisateur:int):
#     curseur = connexion.cursor()
#     curseur.execute("""
#         UPDATE utilisateur
#         SET nom=?, email=?, mdp=?
#         WHERE id=?
#     """, (utilisateur.nom, utilisateur.email, utilisateur.mdp,id_utilisateur))
#     connexion.commit()

# Mise à jour d'un utilisateur existant
async def get_user_id_from_token(token: str):
    curseur = connexion.cursor()    
    curseur.execute("""
        SELECT id FROM utilisateur
        WHERE token=?
    """, (token,))
    resultat = curseur.fetchone()
    if resultat is None:
        raise HTTPException(status_code=401, detail="Token invalide")
    return resultat[0]



@app.put("/mettre_a_jour_utilisateur")
async def mettre_a_jour_utilisateur(utilisateur: Utilisateur, authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Autorisation manquante")

    # Récupération de l'id de l'utilisateur à partir du token JWT
    id_utilisateur = await get_user_id_from_token(authorization)
    connexion = sqlite3.connect('db_trading.db')
    curseur = connexion.cursor()

    # Hash du mot de passe
    mdp_hash = hashlib.sha256(utilisateur.mdp.encode()).hexdigest()

    # Génération du nouveau token
    nouveau_token = secrets.token_hex(16)

    curseur.execute("""
        UPDATE utilisateur
        SET nom=?, email=?, mdp=?, token=?
        WHERE id=?
    """, (utilisateur.nom, utilisateur.email, mdp_hash, nouveau_token, id_utilisateur))
    connexion.commit()

    # Renvoi de l'utilisateur avec son nouveau token
    return {"id": id_utilisateur, "nom": utilisateur.nom, "email": utilisateur.email, "token": nouveau_token}







# @app.put ("/mettre_a_jour_action") #OK
# async def mettre_a_jour_action(action:Action,id_action:int):
#     curseur = connexion.cursor()
#     curseur.execute("""
#         UPDATE action
#         SET prix=?, entreprise=?
#         WHERE id=?
#     """, (action.prix, action.entreprise, id_action))
#     connexion.commit()
    
    
@app.put ("/mettre_a_jour_action") #OK
async def mettre_a_jour_action(action:ActionPrix,entreprise:str):
    connexion = sqlite3.connect('db_trading.db')
    curseur = connexion.cursor()
    curseur.execute("""
        UPDATE action
        SET prix=?
        WHERE entreprise=?
    """, (action.prix,entreprise))
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
# async def supprimer_action(id_action):
#     curseur = connexion.cursor()
#     curseur.execute("""
#         DELETE FROM action
#         WHERE entreprise=?
#     """, (entreprise.entreprise,))
#     connexion.commit()
    
# @app.delete ("/supprimer_action") #OK
async def supprimer_action(entreprise:DeleteAction):
    connexion = sqlite3.connect('db_trading.db')
    curseur = connexion.cursor()
    curseur.execute("""
        DELETE FROM action
        WHERE entreprise=?
    """, (entreprise.entreprise,))
    connexion.commit()
    




@app.delete("/supprimer_asso_suivi_suiveur") 
async def supprimer_asso_suivi_suiveur(id_suivi: int, authorization: str = Header("Authorization")):
    connexion = sqlite3.connect('db_trading.db')

    curseur = connexion.cursor()


    # Récupération de l'id_suiveur correspondant au token JWT
    id_suiveur = await get_user_id_from_token(authorization)

    # Vérification que l'association existe
    curseur.execute("""
        SELECT id_suivi, id_suiveur FROM asso_suivi_suiveur
        WHERE id_suivi=? AND id_suiveur=?
    """, (id_suivi, id_suiveur))
    resultat = curseur.fetchone()
    if resultat is None:
        raise HTTPException(status_code=404, detail="L'association n'existe pas")

    # Suppression de l'association
    curseur.execute("""
        DELETE FROM asso_suivi_suiveur
        WHERE id_suivi=? AND id_suiveur=?
    """, (id_suivi, id_suiveur))
    connexion.commit()

    return {"message": "L'association a été supprimée avec succès"}



