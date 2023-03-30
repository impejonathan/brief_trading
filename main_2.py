from fastapi import FastAPI 
from pydantic import BaseModel  
import sqlite3

connexion = sqlite3.connect('db_trading.db')
app = FastAPI()

# UTILISATEUR ---------------------------------------------------------------------------------------

class Utilisateur(BaseModel):
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

@app.get("/lire_utilisateur_par_id/{id_utilisateur}")
async def lire_utilisateur_par_id(id_utilisateur: int):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM utilisateur
        WHERE id=?
    """, (id_utilisateur,))
    utilisateur = curseur.fetchone()
    return utilisateur

@app.put("/mettre_a_jour_utilisateur/{id_utilisateur}")
async def mettre_a_jour_utilisateur(id_utilisateur: int, utilisateur: Utilisateur):
    curseur = connexion.cursor()
    curseur.execute("""
        UPDATE utilisateur
        SET nom=?, email=?, mdp=?, token=?
        WHERE id=?
    """, (utilisateur.nom, utilisateur.email, utilisateur.mdp, utilisateur.token, id_utilisateur))
    connexion.commit()

@app.delete("/supprimer_utilisateur/{id_utilisateur}")
async def supprimer_utilisateur(id_utilisateur: int):
    curseur = connexion.cursor()
    curseur.execute("""
        DELETE FROM utilisateur
        WHERE id=?
    """, (id_utilisateur,))
    connexion.commit()

# --------------------------------------------------------------------------------------------------------------
class Action(BaseModel):
    prix: float
    entreprise: str

@app.post("/creer_action")
async def creer_action(action: Action):
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

@app.get ("/lire_action_par_id/{id_action}")
async def lire_action_par_id(id_action: int):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM action
        WHERE id=?
    """, (id_action,))
    action = curseur.fetchone()
    return action

@app.put ("/mettre_a_jour_action/{id_action}")
async def mettre_a_jour_action(id_action: int, action: Action):
    curseur = connexion.cursor()
    curseur.execute("""
        UPDATE action
        SET prix=?, entreprise=?
        WHERE id=?
    """, (action.prix, action.entreprise, id_action))
    connexion.commit()

@app.delete ("/supprimer_action/{id_action}")
async def supprimer_action(id_action: int):
    curseur = connexion.cursor()
    curseur.execute("""
        DELETE FROM action
        WHERE id=?
    """, (id_action,))
    connexion.commit()

    
    
# -------------------------------------------------------------------------------------------------------------------------

class AssoUtilisateurAction(BaseModel):
    id_utilisateur: int
    id_action: int

@app.post("/creer_asso_utilisateur_action")
async def creer_asso_utilisateur_action(asso: AssoUtilisateurAction):
    curseur = connexion.cursor()
    curseur.execute("""
        INSERT INTO asso_utilisateur_action(id_utilisateur, id_action)
        VALUES (?, ?)
    """, (asso.id_utilisateur, asso.id_action))
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
async def lire_asso_utilisateur_action_par_id(id_asso_utilisateur_action: int):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM asso_utilisateur_action
        WHERE id_asso_utilisateur_action=?
    """, (id_asso_utilisateur_action,))
    asso_utilisateur_action = curseur.fetchone()
    return asso_utilisateur_action

    
    
# ---------------------------------------------------------
class Asso_suivi_suiveur(BaseModel):
    id_suivi: int
    id_suiveur: int

@app.post("/creer_asso_suivi_suiveur")
async def creer_asso_suivi_suiveur(utilisateur: Asso_suivi_suiveur):
    curseur = connexion.cursor()
    curseur.execute("""
        INSERT INTO asso_suivi_suiveur(id_suivi, id_suiveur)
        VALUES (?,?)
    """, (utilisateur.id_suivi, utilisateur.id_suiveur))
    connexion.commit()
    return {"message": "Association utilisateur-suiveur créée"}

@app.get("/lire_asso_suivi_suiveur_par_suivi")
async def lire_asso_suivi_suiveur_par_suivi(id_suivi: int):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM asso_suivi_suiveur
        WHERE id_suivi=?
    """, (id_suivi,))
    assos = curseur.fetchall()
    return assos

@app.get("/lire_asso_suivi_suiveur_par_suiveur")
async def lire_asso_suivi_suiveur_par_suiveur(id_suiveur: int):
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM asso_suivi_suiveur
        WHERE id_suiveur=?
    """, (id_suiveur,))
    assos = curseur.fetchall()
    return assos

@app.put("/mettre_a_jour_asso_suivi_suiveur")
async def mettre_a_jour_asso_suivi_suiveur(id_asso: int, id_suivi: int = None, id_suiveur: int = None):
    curseur = connexion.cursor()
    update_clause = ""
    update_values = []
    if id_suivi is not None:
        update_clause += "id_suivi=?, "
        update_values.append(id_suivi)
    if id_suiveur is not None:
        update_clause += "id_suiveur=?, "
        update_values.append(id_suiveur)
    if update_clause:
        update_clause = update_clause[:-2]
        update_values.append(id_asso)
        curseur.execute(f"""
            UPDATE asso_suivi_suiveur
            SET {update_clause}
            WHERE id=?
        """, tuple(update_values))
        connexion.commit()
        return {"message": f"Association utilisateur-suiveur avec l'id {id_asso} mise à jour avec succès"}
    else:
        return {"message": "Aucune mise à jour à effectuer"}

@app.delete("/supprimer_asso_suivi_suiveur")
async def supprimer_asso_suivi_suiveur(id_asso: int):
    curseur = connexion.cursor()
    curseur.execute("""
        DELETE FROM asso_suivi_suiveur
        WHERE id=?
    """, (id_asso,))
    connexion.commit()
    return {"message": f"Association utilisateur-suiveur avec l'id {id_asso} supprimée avec succès"}









