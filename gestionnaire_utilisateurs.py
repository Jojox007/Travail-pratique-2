"""
Ce module est responsable de la gestion des utilisateurs dans l'application IFT-1004 DuProprio,
incluant l'enregistrement de nouveaux utilisateurs et la connexion des utilisateurs existants.
Il interagit avec le fichier des utilisateurs pour enregistrer et vérifier les informations des utilisateurs,
tels que les noms d'utilisateurs et les mots de passe (sous forme hachée).

Fonctions:
- `creer_compte()`: Crée un nouveau compte utilisateur.
- `se_connecter()`: Connecte un utilisateur existant en vérifiant son nom d'utilisateur et son mot de passe.
- `se_deconnecter()`: Déconnecte l'utilisateur actuel.
- `utilisateur_est_connecte()`: Vérifie si un utilisateur est connecté.
- `recuperer_utilisateur_courant()`: Récupère l'utilisateur actuellement connecté.
- `definir_utilisateur_courant(nom_utilisateur)`: Définit l'utilisateur actuellement connecté.
- `vider_session()`: Efface les informations de session de l'utilisateur actuellement connecté.

Dépendances:
- `secrets`: Pour comparer les hachages (https://docs.python.org/3/library/secrets.html#secrets.compare_digest).
- `gestionnaire_donnees`: Pour lire et écrire dans le fichier des utilisateurs.
- `utilitaires`: Pour hacher les mots de passe.
- `configuration`: Pour accéder au chemin du fichier de session.
"""

import secrets
from gestionnaire_donnees import charger_utilisateurs, sauvegarder_utilisateurs
from utilitaires import hacher_mot_de_passe
from configuration import FICHIER_SESSION, FICHIER_UTILISATEURS


def recuperer_utilisateur_courant():
    """Récupère l'utilisateur actuellement connecté.

    Returns:
        str or None: Le nom d'utilisateur actuellement connecté, ou None s'il n'y a pas d'utilisateur connecté.
    """
    try:
        fichier = open(FICHIER_SESSION, 'r')
        nom_utilisateur = fichier.read()
        fichier.close()
        if nom_utilisateur == "":
            return None
        return nom_utilisateur
    except FileNotFoundError:
        return print("Aucun utilisateur connecté.")


def definir_utilisateur_courant(nom_utilisateur):
    """Définit l'utilisateur actuellement connecté.

    Args:
        nom_utilisateur (str): Le nom d'utilisateur à connecter.

    Cette fonction écrit le nom de l'utilisateur dans le fichier de session,
    marquant ainsi cet utilisateur comme étant actuellement connecté.
    """
    fichier = open(FICHIER_SESSION, 'w')
    fichier.write(nom_utilisateur)


def vider_session():
    """Efface les informations de session de l'utilisateur actuellement connecté.

    Cette fonction vide le fichier de session, déconnectant ainsi l'utilisateur en cours.
    """
    open(FICHIER_SESSION, 'w').close()

def creer_compte():
    """Crée un nouveau compte utilisateur.

    Demande à l'utilisateur un nom d'utilisateur et un mot de passe, hache le mot de passe et sauvegarde les
    informations dans le fichier des utilisateurs. Si le nom d'utilisateur est déjà pris, un message d'erreur approprié
    devra être affiché.
    """

    # demander a l'utilisateur son nom et son mot de passe
    username = input("Nom d'utilisateur:")
    ## verifier si le nom d'utilisateur existe deja
    utilisateurs_deja_existant = charger_utilisateurs()

    if utilisateurs_deja_existant is None:
        utilisateurs_deja_existant = {}

    while username in utilisateurs_deja_existant:
        print("Nom d'utilisateur déjà pris. Veuillez en choisir un autre.")
        username = input("Nom d'utilisateur:")

    password = input("Mot de passe:")
    mot_de_passe_hache = hacher_mot_de_passe(password)

    ## sauvegarder les informations dans le fichier des utilisateurs
    utilisateur_a_sauvegarder = {username: mot_de_passe_hache}
    sauvegarder_utilisateurs(utilisateur_a_sauvegarder)


def se_connecter():
    """Connecte un utilisateur existant.

    Demande à l'utilisateur un nom d'utilisateur et un mot de passe, hache le mot de passe et vérifie les informations
    dans le fichier des utilisateurs. Si les informations sont correctes, l'utilisateur est connecté.
    """
    # Demande à l'utilisateur un nom d'utilisateur et un mot de passe,

    # partie utilisateur
    username = input("Nom d'utilisateur:")
    tout_mes_utilisateurs = charger_utilisateurs()

    if username in tout_mes_utilisateurs:
        print("utilisateur existe")
    else:
        print("utilisateur n'existe pas")
        return

    # partie mot de passe
    password = input("Mot de passe:")
    mdp_hache = hacher_mot_de_passe(password)

    # verifier si le mot de passe est correcte
    mot_de_passe_du_fichier_hache = tout_mes_utilisateurs[username]
    if mdp_hache == mot_de_passe_du_fichier_hache:
        print("connexion réussie")
        definir_utilisateur_courant(username)
    else:
        print("mot de passe incorrect")


def se_deconnecter():
    """Déconnecte l'utilisateur actuel."""
    vider_session()
    print("Déconnexion réussie.")


def utilisateur_est_connecte():
    """Vérifie si un utilisateur est connecté.

    Returns:
        bool: True si un utilisateur est connecté, False sinon.
    """
    return recuperer_utilisateur_courant() is not None