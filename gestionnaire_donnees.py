"""
Ce module est responsable de la gestion des données de l'application IFT-1004 DuProprio,
incluant le chargement et la sauvegarde des utilisateurs et des propriétés dans des fichiers JSON.

Fonctions:
- `charger_utilisateurs()`: Charge les utilisateurs depuis le fichier des utilisateurs.
- `sauvegarder_utilisateurs(utilisateurs)`: Sauvegarde les utilisateurs dans le fichier des utilisateurs.
- `charger_proprietes()`: Charge toutes les propriétés depuis le fichier des propriétés.
- `sauvegarder_propriete(new_property)`: Sauvegarde une nouvelle propriété.

Dépendances:
- `json`: Pour lire et écrire des fichiers JSON.
- `configuration`: Pour accéder à des constantes globales comme les chemins des fichiers.
"""

import json
from configuration import FICHIER_UTILISATEURS, FICHIER_PROPRIETES


# defrom gestionnaire_utilisateurs import creer_compte
def charger_utilisateurs():
    """Charge les utilisateurs depuis le fichier des utilisateurs.

    Returns:
        dict: Un dictionnaire des utilisateurs avec leurs mots de passe hachés.
    """
    try:
        with open(FICHIER_UTILISATEURS, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def sauvegarder_utilisateurs(utilisateurs):
    """Sauvegarde les utilisateurs dans le fichier des utilisateurs.

    Args:
        utilisateurs (dict): Un dictionnaire des utilisateurs avec leurs mots de passe hachés.
    """

    utilisateurs_deja_existant = charger_utilisateurs()

    if utilisateurs_deja_existant is None:
        utilisateurs_deja_existant = {}


    u_t = {**utilisateurs, **utilisateurs_deja_existant}

    with open(FICHIER_UTILISATEURS, "w") as f:
        json.dump(u_t, f)


def charger_proprietes():
    """Récupère toutes les propriétés disponibles.

    Returns:
        list: Liste des propriétés.
    """
    try:
        with open(FICHIER_PROPRIETES, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def sauvegarder_propriete(nouvelle_propriete):
    """Sauvegarde une nouvelle propriété.

    Args:
        nouvelle_propriete (dict): Dictionnaire contenant les informations de la nouvelle propriété.
    """

    propriete_deja_existant = charger_proprietes()

    if propriete_deja_existant is None:
       propriete_deja_existant = {}

    proprio = {propriete_deja_existant}

    with open(FICHIER_PROPRIETES, "w") as f:
        json.dump(proprio, f)